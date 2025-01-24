from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChatSession
from .serializers import ChatSessionSerializer
from .chatbot import recommend_games, generate_bot_response
from django.contrib.auth.models import User


# # 공통 사용자 확인 함수
def get_user_from_request(request):
    user_id = request.data.get('user_id') or request.query_params.get('user_id')
    if not user_id:
        return None, {"error": "user_id is required"}, status.HTTP_400_BAD_REQUEST

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None, {"error": "User not found"}, status.HTTP_404_NOT_FOUND

    return user, None, None



class LoadSessionView(APIView):
    def get(self, request):
        # 유저 정보 가져오기 (예: request.user 또는 JWT 토큰)
        # user, error, status_code = get_user_from_request(request)
        # if error:
        #     return Response({"error": error}, status=status_code)

        # 해당 유저의 모든 세션 가져오기
        # sessions = ChatSession.objects.filter(user=user).order_by("-created_at")
        sessions = ChatSession.objects.order_by("-created_at")

        # 직렬화하여 반환
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LoadSessionMessagesView(APIView):
    def get(self, request, session_id):
        # user, error, status_code = get_user_from_request(request)
        # if error:
        #     return Response({"error": error}, status=status_code)

        try:
            # chat_session = ChatSession.objects.get(id=session_id, user=user)
            chat_session = ChatSession.objects.get(id=session_id)
        except ChatSession.DoesNotExist:
            return Response({"error": "Session not found or user mismatch"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProcessSessionView(APIView):
    def post(self, request):
        # 유저 정보 확인
        # user, error, status_code = get_user_from_request(request)
        # if error:
        #     return Response(error, status=status_code)

        # 요청 데이터 가져오기
        user_input = request.data.get('user_input')
        session_id = request.data.get('session_id')

        if not user_input:
            return Response({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # 이전 세션이 있을 경우 메시지들 불러오기
        if session_id:
            try:
                # chat_session = ChatSession.objects.get(id=session_id, user=user)
                chat_session = ChatSession.objects.get(id=session_id)
                # 세션에 있는 메시지들 가져오기
                previous_messages = chat_session.messages
            except ChatSession.DoesNotExist:
                return Response({"error": "Session not found or user mismatch"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 세션이 없으면 빈 리스트
            previous_messages = []

        
        # 'generate_bot_response'에 이전 대화와 유저 입력을 전달하여 봇의 응답 생성
        bot_response = generate_bot_response(previous_messages, user_input)

        # 응답이 리스트 형태일 경우, 문자열로 변환
        if isinstance(bot_response, list):
            bot_response = " ".join([str(item) for item in bot_response])

        # 세션 메시지에 따로 따로 넣기
        user_message = {"role": "user", "content": user_input}
        chatbot_message = {"role": "chatbot", "content": bot_response}

        # session_id가 있으면 기존 세션 업데이트, 없으면 새 세션 생성
        if session_id:
            try:
                # 기존 세션에 각각 따로 메시지 추가
                chat_session.messages.append(user_message)
                chat_session.messages.append(chatbot_message)
                chat_session.save()
            except ChatSession.DoesNotExist:
                return Response({"error": "Session not found or user mismatch"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # 새로운 세션 생성 시, 각각 따로 메시지 추가
            chat_session = ChatSession.objects.create(messages=[user_message, chatbot_message])

        # 직렬화하여 응답 반환
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)





class StartSessionView(APIView):
    def post(self, request):
        # user, error, status_code = get_user_from_request(request)
        # if error:
        #     return Response(error, status=status_code)

        message = request.data.get('user_input')
        if not message:
            return Response({"error": "message is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the recommended games based on the message
        recommended_games = recommend_games(message)
        
        if not recommended_games:
            return Response({"error": "No game recommendations found."}, status=status.HTTP_404_NOT_FOUND)

        # Create a new ChatSession and save it to the database
        chat_session = ChatSession.objects.create(
            # user=user,  # 주석 제거 후 실제 유저를 연결
            messages=[
                {"role": "user", "content": message},
                {"role": "bot", "content": recommended_games},
            ]
        )

        # Serialize the chat session and return the response
        serializer = ChatSessionSerializer(chat_session)
        return Response(serializer.data, status=status.HTTP_201_CREATED)