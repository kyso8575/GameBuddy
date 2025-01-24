import streamlit as st
import requests

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "Start"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_logs" not in st.session_state:
    st.session_state.session_logs = []
if "current_message" not in st.session_state:
    st.session_state.current_message = []


def load_sessions():
    user_id = st.session_state.get("user_id", 1)  # 세션에 저장된 유저 ID 사용
    if user_id:
        response = requests.get(f"http://127.0.0.1:8000/chatbot/load_session/")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to load sessions.")
    return []

def sidebar_sessions():
    st.sidebar.title("Chat History")
    
    # 세션을 불러오는 함수 (예시로 가정)
    sessions = load_sessions()

    if not sessions:
        st.sidebar.write("No sessions available.")
        return

    for idx, session in enumerate(sessions):
        # 세션에서 id와 messages 추출 (딕셔너리에서 접근)
        session_id = session.get("id")
        session_messages = session.get("messages")
        st.session_state.is_loaded = False

        button_label = session_messages[0]["content"][:12] + '...' if session_messages and len(session_messages) > 0 else "No messages"

        if st.sidebar.button(button_label, key=f"Session {idx + 1}"):
            # 세션 ID와 메시지를 세션 상태에 저장
            st.session_state.selected_session_id = session_id
            st.session_state.messages = session_messages  # 세션의 대화 내용
            st.session_state.current_page = "Chat"

def load_session_messages(session_id):
    response = requests.get(f"http://127.0.0.1:8000/chatbot/session/{session_id}/")
    if response.status_code == 200:
        return response.json().get("messages", [])
    else:
        st.error("Failed to load session messages.")
        return []


def get_bot_response(user_input):
    # 실제 챗봇 로직을 넣을 부분 (추천 게임 로직 등)
    return f"This is a response to your input: {user_input}"


def start_page():
    sidebar_sessions()  # 사이드바에서 기존 세션 표시

    st.title("🎮 Welcome to the Game Recommendation Chatbot")
    st.write("Enter your preferences below and click the button to start chatting and get game recommendations!")

    user_input = st.text_input("Enter your preferences:", "", key="preferences_input", help="E.g., genre, platform, age group")

    if st.button("Start Chatting"):
        if user_input:
            # 새로운 세션 생성 요청
            response = requests.post("http://127.0.0.1:8000/chatbot/start_session/", json={"user_input": user_input})
            if response.status_code == 200 | response.status_code == 201:
                session_data = response.json()
                st.session_state.selected_session_id = session_data["id"]  # 새로운 세션 ID 저장
                st.session_state.messages = session_data["messages"]  # 초기 메시지 저장
                st.session_state.current_page = "Chat"  # Chat 페이지로 이동
            else:
                st.error("Failed to initialize chat. Please try again.")
        else:
            st.warning("Please enter your preferences before starting.")


def chat_page():
    # 사이드바에서 기존 세션 표시
    sidebar_sessions()

    # 페이지 제목
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 Game Recommendation Chatbot</h1>", unsafe_allow_html=True)

    # 선택된 세션의 대화 내역 가져오기
    if "selected_session_id" in st.session_state:
        if "messages" not in st.session_state:
            # 세션 ID를 기반으로 초기 메시지 가져오기
            st.session_state.messages = load_session_messages(st.session_state.selected_session_id)

        # 대화 내역을 위한 스타일 정의2
        st.markdown(
            """
            <style>
                .chat-container {
                    padding: 1px;
                    border-radius: 5px;
                    background-color: #f9f9f9;
                    margin-bottom: 20px;
                }
                .chat-message {
                    display: flex;
                    align-items: center;
                    margin-bottom: 15px;
                }
                .chat-icon {
                    font-size: 24px;
                    margin-right: 10px;
                }
                .chat-icon.right {
                    margin-left: 10px;
                    margin-right: 0;
                }
                .user-message {
                    background-color: #dff9fb;
                    color: #130f40;
                    padding: 10px;
                    border-radius: 10px;
                    max-width: 70%;
                    display: inline-block;
                }
                .bot-message {
                    background-color: #f1f2f6;
                    color: #2f3640;
                    padding: 10px;
                    border-radius: 10px;
                    max-width: 70%;
                    display: inline-block;
                }
                .user-container {
                    justify-content: flex-start;
                }
                .bot-container {
                    justify-content: flex-end;
                }
            </style>
            """, 
            unsafe_allow_html=True
        )

        # 대화 내역 출력
        chat_history = st.container()
        with chat_history:
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state.messages:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-message user-container">
                            <div class="chat-icon">👤</div>
                            <div class="user-message">{msg['content']}</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-message bot-container">
                            <div class="bot-message">{msg['content']}</div>
                            <div class="chat-icon right">🤖</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.warning("No session selected. Please start a session from the sidebar or the start page.")

    # 새로운 메시지 입력
    user_input = st.text_input("Your Message", "", key="user_input", help="Type your message here")

    if user_input:
        # 유저 메시지 저장
        st.session_state.current_message = [{"role": "user", "content": user_input}]

        # POST 요청을 통해 봇 응답 받기
        try:
            response = requests.post(
                "http://127.0.0.1:8000/chatbot/process_session/",
                json={"user_input": user_input, "session_id": st.session_state.selected_session_id}
            )
            # 응답 상태 코드 확인
            if response.status_code == 200 or response.status_code == 201:
                # Extract the 'messages' from the response
                messages_data = response.json().get("messages", None)
                if messages_data:
                    # Find the latest message from the chatbot
                    bot_response = None
                    for msg in reversed(messages_data):
                        if msg.get("role") == "chatbot":
                            bot_response = msg.get("content", "No content")
                            break
                          
                    # If bot response is found, format it accordingly
                    if isinstance(bot_response, list):
                        bot_response = " ".join([str(item) if isinstance(item, str) else str(item.get('content', '')) for item in bot_response])

                    # Add the bot's response to the session state messages
                    st.session_state.current_message.append({"role": "bot", "content": bot_response})
                else:
                    # If no messages are found, append a default error message
                    st.session_state.current_message.append({"role": "bot", "content": "No messages from bot."})
            else:
                # Handle error when response status is not successful
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
              # Catch any exceptions and display the error
              st.error(f"An error occurred: {str(e)}")


        # 업데이트된 메시지 출력
        chat_history.empty()  # 이전 내역 제거
        with chat_history:
            st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
            for msg in st.session_state.current_message:
                if msg["role"] == "user":
                    st.markdown(
                        f"""
                        <div class="chat-message user-container">
                            <div class="chat-icon">👤</div>
                            <div class="user-message">{msg['content']}</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="chat-message bot-container">
                            <div class="bot-message">{msg['content']}</div>
                            <div class="chat-icon right">🤖</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
            st.markdown("</div>", unsafe_allow_html=True)





def main():
    st.set_page_config(page_title="Game Recommendation Chatbot", page_icon="🎮")

    if st.session_state.current_page == "Start":
        start_page()
    elif st.session_state.current_page == "Chat":
        chat_page()



if __name__ == "__main__":
    main()




