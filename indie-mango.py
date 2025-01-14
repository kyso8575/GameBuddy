import openai
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import uuid
import requests  # FastAPI와 통신
import logging
import subprocess
import time

########### FastAPI 서버 URL 선언 / 로그파일 생성 ###################
API_BASE_URL = "http://127.0.0.1:8003"  # FastAPI 서버 로컬 호스트 값
# API_BASE_URL = "http://0.0.0.0:8000"  # FastAPI 서버 외부 연결 시

logging.basicConfig(
    filename="Client_UI.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Streamlit UI started.")

################# FastAPI 서버 실행 #################################
subprocess.Popen(["uvicorn", "v1_API_server:app", "--reload", "--port", "8003"])

def wait_for_api():
    while True:
        try:
            response = requests.get(f"{API_BASE_URL}/server_check")  # health_check 엔드포인트를 통해 서버 상태 확인
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            time.sleep(1)  # 서버가 준비될 때까지 1초 간격으로 반복
    
wait_for_api()
####################### OpenAI API키 호출 ###########################
# .env 파일에서 api 키 가져오기
load_dotenv()
API_KEY = os.getenv('openai_api_key')
if API_KEY:
    openai.api_key = API_KEY
else:
    st.error("API 키가 설정되지 않았습니다. .env 파일을 확인하세요.")
    st.stop()
####################### DB 로드 ###########################
# CSV 파일 로드
CSV_FILE = "chat_history.csv"
# CSV 파일이 존재하면 불러오기, 없으면 새로 생성
try:
    chat_history_df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    chat_history_df = pd.DataFrame(columns=["ChatID", "Role", "Content"])

# 페이지 구성
st.set_page_config(
    page_title='MANGO',
    page_icon='<i class="fa-solid fa-gamepad"></i>',
    layout='wide',
    initial_sidebar_state='auto'
)

# 각 세션
if "login" not in st.session_state:
    st.session_state.login = False
if "page" not in st.session_state:
    st.session_state.page = "LOGIN"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 로그인 검증 함수
def login(user_id, password):
    # ID와 비밀번호를 간단히 하드코딩
    correct_id = "admin"
    correct_password = "password123"
    return user_id == correct_id and password == correct_password

# 페이지 전환 함수
def set_page(page_name):
    st.session_state.page = page_name

# 로그아웃 함수
def logout():
    st.session_state.login = False
    st.session_state.page = "LOGIN"

# 메인 화면
if st.session_state.page == "LOGIN":
    st.title("Login Page")
    user_id = st.text_input("User ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login(user_id, password):
            st.session_state.login = True
            st.session_state.page = "HOME"
            st.success("로그인 성공! 홈으로 이동합니다.")
        else:
            st.error("아이디 또는 비밀번호가 잘못되었습니다.")

elif st.session_state.page == "HOME":
    if st.session_state.login:
        st.title("Welcome to the HOME Page!")
        st.write("홈 페이지에서 검색과 챗봇 기능을 사용할 수 있습니다.")

        # 검색창 추가
        search_query = st.text_input("검색창", placeholder="검색어를 입력하세요...")
        if st.button("검색"):
            st.write(f"'{search_query}'에 대한 검색 결과는 다음과 같습니다.")
            # 여기에 검색 로직 추가 가능 (예: 데이터베이스 검색)

        # 챗봇 세션 추가
        st.subheader("챗봇과 대화하기")
        user_message = st.text_input("메시지 입력", key="user_message")
        if st.button("전송", key="send_button"):
            if user_message:
                # 챗봇 API 호출
                bot_response = query_llm(user_message)
                # 대화 기록 업데이트
                st.session_state.chat_history.append(("user", user_message))
                st.session_state.chat_history.append(("bot", bot_response))

        # 대화 기록 출력
        st.write("### 대화 기록")
        for sender, message in st.session_state.chat_history:
            if sender == "user":
                st.write(f"**사용자**: {message}")
            else:
                st.write(f"**챗봇**: {message}")
    else:
        st.warning("먼저 로그인해주세요.")
        st.session_state.page = "LOGIN"

elif st.session_state.page == "SIGNUP":
    st.title("Signup Page")
    st.write("회원가입 페이지")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        st.success(f"{name}님, 회원가입이 완료되었습니다!")

# 외부 LLM API 호출 함수
def query_llm(prompt):
    """
    외부 LLM 챗봇 API에 프롬프트를 보내고 응답을 받아옵니다.
    여기에 적합한 API URL과 헤더/파라미터를 설정하세요.
    """
    try:
        api_url = "https://your-llm-api-url.com/chat"  # 실제 API URL로 변경
        headers = {"Authorization": "Bearer YOUR_API_KEY"}  # 필요 시 인증 추가
        data = {"prompt": prompt}
        response = requests.post(api_url, json=data, headers=headers)
        response.raise_for_status()
        return response.json().get("response", "응답을 가져올 수 없습니다.")
    except Exception as e:
        return f"오류 발생: {e}"

# 사이드바
with st.sidebar:
    if st.session_state.login:
        if st.button("LOGOUT"):
            logout()
    else:
        if st.button("LOGIN"):
            set_page("LOGIN")
    if st.button("HOME"):
        set_page("HOME")
    if st.button("SIGNUP"):
        set_page("SIGNUP")