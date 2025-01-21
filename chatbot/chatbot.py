from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from games.models import Game
import os
from dotenv import load_dotenv
import re
import json
from django.db.models.functions import Lower
from django.db.models import Q
import ast
from functools import reduce


# 환경 변수 로드
load_dotenv()



def get_all_unique_values():
    """
    platforms, esrb_ratings, stores, genres의 고유 값을 가져옵니다.
    """
    unique_platforms = Game.objects.values_list('platforms', flat=True).distinct()
    unique_esrb_ratings = Game.objects.values_list('esrb_rating', flat=True).distinct()
    unique_stores = Game.objects.values_list('stores', flat=True).distinct()
    unique_genres = Game.objects.values_list('genres', flat=True).distinct()

    return {
        "platforms": [str(item) for item in unique_platforms],
        "esrb_ratings": [str(item) for item in unique_esrb_ratings],
        "stores": [str(item) for item in unique_stores],
        "genres": [str(item) for item in unique_genres],
    }


# 모델 초기화
model = ChatOpenAI(model="gpt-4o-mini")
# 환경 변수에서 API 키 가져오기

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")


# 모델 초기화

unique_values = get_all_unique_values()
    
# 각 리스트를 문자열로 변환
platform_list_str = ", ".join(unique_values['platforms'])
esrb_list_str = ", ".join(unique_values['esrb_ratings'])
store_list_str = ", ".join(unique_values['stores'])
genre_list_str = ", ".join(unique_values['genres'])


# ChatPromptTemplate 구성
parse_prompt_template = ChatPromptTemplate.from_messages([
    ("system", f"""
    당신은 사용자의 입력에서 게임 추천을 위한 정보를 추출하는 전문가입니다. 
    사용자의 텍스트에서 아래 조건에 따라 정보를 추출하고, 정확히 지정된 형식으로 반환하세요.
    각 주제들은 여러 개의 값을 가질 수 있습니다.

    **조건**
    1. 장르는 반드시 아래 리스트 안에서 반환하세요. 비슷한 모든 장르 여러개를 포함하세요. 없으면 '알 수 없음'으로 반환하세요:
       - {genre_list_str}
    2. ESRB 등급(esrb_ratings)은 반드시 리스트 안에서 반환하세요. 없으면 '알 수 없음'으로 반환하세요:
       - {esrb_list_str}
    3. 플랫폼은 반드시 리스트 안에서 반환하세요. 비슷한 모든 플랫폼들 여러개를 포함시키세요. 없으면 '알 수 없음'으로 반환하세요:
       - {platform_list_str}
    4. 출시일(released) 정보가 없으면 '알 수 없음'으로 반환하세요.
    5. 게임을 구매할 수 있는 상점(stores)은 반드시 리스트 안에서 반환하세요. 없으면 '알 수 없음'으로 반환하세요:
       - {store_list_str}
    
       
    
    출력 형식: 
    - 장르: (추출된 여러 장르 또는 '알 수 없음')
    - 플랫폼: (추출된 여러 플랫폼 또는 '알 수 없음')
    - 출시일: (추출된 출시일 또는 '알 수 없음')
    - 상점: (추출된 여러 상점 또는 '알 수 없음')
    - ESRB 등급: (추출된 여러 ESRB 등급 또는 '알 수 없음')
    
    사용자 입력과 무관한 값이나 지정된 범위를 벗어난 값은 절대 포함하지 마세요.
    """),
    ("user", """
    입력: "{user_input}"
     
    """)
])


response_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
    당신은 사용자에게 게임 추천 메시지를 작성하는 전문가입니다. 
    입력된 추천 게임 목록을 기반으로, 각 게임에 대한 간략한 설명을 포함한 추천 메시지를 작성하세요.

    **규칙**
    1. 각 게임에 대해 간단하고 흥미로운 설명을 작성하세요. 설명은 게임의 장르, 특징, 또는 재미 요소를 포함해야 합니다.
    2. 게임 목록에 주어진 순서를 유지하여 각 게임에 대한 설명을 작성하세요.
    3. 모든 게임을 포함하며, 사용자에게 친근하고 매력적인 어조로 작성하세요.
    4. 설명이 없거나 정보가 부족한 경우, "이 게임은 다양한 모험과 재미를 제공합니다."와 같은 일반적인 문구를 사용하세요.

    """),
    ("user", """
    다음은 추천할 만한 게임 목록입니다:
    {game_list}

    각 게임에 대해 간략한 설명을 추가해주세요.
    """)
])


process_prompt_template = ChatPromptTemplate.from_messages([
    ("system", """
        당신은 사용자의 입력에서 게임 추천을 위한 정보를 추출하는 전문가입니다.
        이전 대화 내용을 바탕으로 user input에 대한 적절한 답변을 해 주세요.
    """),
    ("user", """
        입력: "{user_input}"
    """)
])


def _parse_list(value):
    """
    문자열을 Python 리스트로 변환하는 헬퍼 함수.
    "알 수 없음"이나 빈 값은 빈 리스트로 처리.
    """
    try:
        if value and value != '알 수 없음' and value != '[]':
            # JSON 파싱 대신 Python 리스트 문자열을 처리
            return ast.literal_eval(value) if isinstance(value, str) else value
        return []
    except (ValueError, SyntaxError):
        return []  # 변환 실패 시 빈 리스트 반환


def parse_user_input(user_input):
    """
    유저 입력을 파싱하여 장르, 연령 제한, 플랫폼, 출시일, 플레이타임, 상점, ESRB 등급 정보를 추출하고,
    JSON 형식으로 반환합니다.
    """

    # 프롬프트를 사용자 입력으로 포맷
    prompt = parse_prompt_template.format_messages(user_input=user_input)
    response = model.invoke(prompt)

    try:
        # 정규식: 각 항목을 파싱하도록 확장
        match = re.search(
            r"-\s*장르:\s*(\[.*?\]|.*)\n"
            r"-\s*플랫폼:\s*(\[.*?\]|.*)\n"
            r"-\s*출시일:\s*(.*?)\n"
            r"-\s*상점:\s*(\[.*?\]|.*)\n"
            r"-\s*ESRB 등급:\s*(\[.*?\]|.*)",
            response.content
        )

        if not match:
            raise ValueError(f"응답 형식이 예상과 다릅니다. 응답: {response.content}")

        # 매칭된 그룹에서 값 추출
        result = {
            "장르": match.group(1),
            "플랫폼": match.group(2),
            "출시일": match.group(3),
            "스토어": match.group(4),
            "연령제한": match.group(5),
        }

        # "알 수 없음" 처리를 JSON에 포함
        for key, value in result.items():
            if value.lower() in ["알 수 없음", "unknown", "none"]:
                result[key] = "알 수 없음"

        return result

    except Exception as e:
        raise ValueError(f"Failed to parse user input. Error: {e}") from e




# 데이터베이스 필터링

def filter_games(answer):
    """
    Django ORM을 사용하여 조건에 맞는 게임 데이터를 필터링하고,
    metacritic_score를 기준으로 정렬하여 상위 3개 결과를 반환합니다.
    """

    try:
        genre_str = answer.get("장르")
        age_limits_str = answer.get("연령제한")
        platforms_str = answer.get("플랫폼")
        stores_str = answer.get("스토어")

        # "알 수 없음" 처리 및 값 변환
        genre = _parse_list(genre_str)
        age_limits = _parse_list(age_limits_str)
        platforms = _parse_list(platforms_str)
        stores = _parse_list(stores_str)


        # ORM 필터링 후 metacritic_score 기준으로 정렬
        queryset = Game.objects.filter(
            # 장르 필터 (OR 조건으로 변경, 부분 일치)
            Q() if not genre else reduce(lambda q, g: q | Q(genres__icontains=g), genre, Q()),

            # 연령제한 필터 (전체 선택 가능)
            Q() if not age_limits else Q(esrb_rating__in=age_limits),

            # 플랫폼 필터 (OR 조건으로 변경, 부분 일치)
            Q() if not platforms else reduce(lambda q, p: q | Q(platforms__contains=[p]), platforms, Q()),

            # 스토어 필터 (OR 조건으로 변경, 부분 일치)
            Q() if not stores else reduce(lambda q, s: q | Q(stores__contains=[s]), stores, Q())
        ).order_by('-metacritic_score')  # metacritic_score를 기준으로 내림차순 정렬

        # 상위 3개 결과만 반환
        top_3_games = queryset[:3]

        return top_3_games

    except Exception as e:
        print(f"디버깅: {answer}")  # 디버깅용 입력 값 출력
        raise ValueError(f"알 수 없는 오류 발생: {e}")




# RAG로 챗봇 응답 생성
def generate_response(filtered_games):
    """
    필터링된 게임 목록을 사용해 추천 메시지를 생성합니다.
    """
    if not filtered_games.exists():
        return "죄송합니다. 요청하신 조건에 맞는 게임을 찾을 수 없습니다."

    game_list = "\n".join([game.name for game in filtered_games])
    prompt = response_prompt_template.format_messages(game_list=game_list)
    response = model.invoke(prompt)
    return response.content


# 메인 함수
def recommend_games(user_input):
    """
    유저 입력을 받아 게임을 추천합니다.
    """
    # 1. 프롬프트 엔지니어링
    parsed_user_input = parse_user_input(user_input)


    # 2. 데이터 필터링
    filtered_games = filter_games(parsed_user_input)

    # 3. 챗봇 응답 생성
    response = generate_response(filtered_games)
    return response


def generate_bot_response(messages, user_input):
    """
    GPT API를 호출하여 문맥 기반 답변 생성.
    """
    try:
        # 이전 메시지를 LangChain 형식으로 포맷
        formatted_messages = []
        for msg in messages:
            # 'role'과 'content'가 존재하는지 확인하고, 없으면 건너뛰기
            if "role" in msg and "content" in msg:
                formatted_messages.append(msg)

        # 프롬프트 포맷팅
        prompt = process_prompt_template.format_messages(user_input=user_input)

        # 프롬프트가 리스트인 경우 문자열로 변환
        if isinstance(prompt, list):
            prompt = " ".join([str(item) for item in prompt])

        # 'role: content' 형식으로 포맷된 메시지 리스트 생성
        formatted_message_strings = []
        for msg in formatted_messages:
            if 'role' in msg and 'content' in msg:
                # content가 리스트일 경우 문자열로 변환
                content = msg['content']
                if isinstance(content, list):
                    content = " ".join([str(item) if isinstance(item, str) else str(item.get('content', '')) for item in content])
                formatted_message_strings.append(f"{msg['role']}: {content}")

        # \n으로 구분된 메시지와 prompt를 결합
        prompt_with_context = "\n".join(formatted_message_strings) + "\n" + prompt

        # 모델 호출 (여기서 base_messages는 list of dict 형태로 전달됨)
        response = model.invoke(prompt_with_context)  # Pass the prompt_with_context directly as a string

        # LangChain의 응답에서 텍스트 추출
        bot_response = response.content
        
        # 응답이 리스트 형태일 경우, 문자열로 변환
        if isinstance(bot_response, list):
            bot_response = " ".join([str(item) if isinstance(item, str) else str(item.get('content', '')) for item in bot_response])

        return bot_response
    except Exception as e:
        return f"Error: {str(e)}"