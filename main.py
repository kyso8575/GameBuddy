import streamlit as st
import yaml
import os
import bcrypt

# 비밀번호를 해시화하는 함수
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

# 비밀번호 검증 함수
def check_password(stored_password: str, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# YAML 파일에서 사용자 정보 로드 함수 (리스트로 반환)
def load_users_from_yaml(filename="config.yaml"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return yaml.safe_load(file) or []
            except yaml.YAMLError as e:
                print(f"YAML 파일 로드 오류: {e}")
                return []
    return []

# YAML 파일에 사용자 저장 함수 (리스트에 추가)
def save_to_yaml(users, filename="config.yaml"):
    with open(filename, "w") as file:
        yaml.dump(users, file, default_flow_style=False)

# YAML 파일에서 사용자 삭제 함수
def delete_user_from_yaml(username, filename="config.yaml"):
    users = load_users_from_yaml(filename)
    user_found = False
    
    # 사용자 목록에서 해당 사용자 찾기
    for user in users:
        if user["username"] == username:
            users.remove(user)
            user_found = True
            break

    if user_found:
        save_to_yaml(users, filename)  # 변경 사항 저장
        return True
    return False

# 초기 세션 상태 설정
if "registration_active" not in st.session_state:
    st.session_state["registration_active"] = False
if "login_active" not in st.session_state:
    st.session_state["login_active"] = False
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None
if "delete_account_active" not in st.session_state:
    st.session_state["delete_account_active"] = False

# 사이드바 버튼 설정
with st.sidebar:
    if st.button("망고 홈페이지"):
        st.session_state["registration_active"] = False
        st.session_state["login_active"] = False
        st.session_state["deletion_active"] = False

    if not st.session_state["logged_in"]:
        if not st.session_state["registration_active"]:
            if st.button("회원가입"):
                st.session_state["registration_active"] = True
                st.session_state["login_active"] = False
        if not st.session_state["login_active"]:
            if st.button("로그인"):
                st.session_state["login_active"] = True
                st.session_state["registration_active"] = False
    else:
        st.sidebar.markdown(f"**환영합니다, {st.session_state['current_user']}님!**")
        if st.button("로그아웃"):
            st.session_state["logged_in"] = False
            st.session_state["current_user"] = None
            st.success("로그아웃 되었습니다.")
        if not st.session_state["deletion_active"]:
            if st.button("회원탈퇴"):
                st.session_state["deletion_active"] = True
                st.rerun()


# 메인 화면
if not st.session_state["registration_active"] and not st.session_state["login_active"] and not st.session_state["deletion_active"]:
    st.title("망고 홈페이지")

    # 닉네임 표시
    if st.session_state["logged_in"]:
        st.markdown(f"### 환영합니다, {st.session_state['current_user']}님! 😊")

    # 이미지 표시
    st.image(
        "https://www.chemicalsafetyfacts.org/wp-content/uploads/shutterstock_609086588-scaled-1-800x400.jpg",  # 이미지예시
        caption="망고 사진 (예제 이미지)", 
        use_container_width=True
    )
    st.divider()
    
    st.text_input("검색할 게임의 정보를 입력해주세요.")
    if st.button("검색"):
        pass

# 회원가입 처리
if st.session_state["registration_active"]:
    st.title("회원가입")
    
    with st.form("registration_form"):
        username = st.text_input("아이디 (Username)")
        password = st.text_input("비밀번호 (Password)", type="password")
        confirm_password = st.text_input("비밀번호 확인 (Confirm Password)", type="password")
        nickname = st.text_input("닉네임 (Nickname)")
        age = st.number_input("나이 (Age)", min_value=1, step=1)
        gender = st.selectbox("성별 (Gender)", ["남성", "여성", "기타"])
        
        # 제출 버튼과 취소 버튼
        submitted = st.form_submit_button("가입")
        cancelled = st.form_submit_button("취소")
        
        if submitted:
            if password != confirm_password:
                st.error("비밀번호가 일치하지 않습니다.")
            elif not username or not password:
                st.error("아이디와 비밀번호는 필수 입력 항목입니다.")
            else:
                # 기존 유저 목록 로드
                users = load_users_from_yaml()

                # 새로운 유저 정보 추가
                new_user = {
                    "username": username,
                    "password": hash_password(password),  # 비밀번호 해시
                    "nickname": nickname,
                    "gender": gender,
                    "age": age,
                }
                
                # 유저 정보를 기존 목록에 추가
                users.append(new_user)
                
                # 저장
                save_to_yaml(users)
                
                # 로그인 처리
                st.session_state["logged_in"] = True
                st.session_state["current_user"] = username
                st.session_state["registration_active"] = False
                st.session_state["login_active"] = False
                
                st.success(f"회원가입이 완료되었습니다. {nickname}님, 환영합니다!")
                st.rerun()
        elif cancelled:
            st.session_state["registration_active"] = False  # 회원가입 세션 취소


# 로그인 처리
if st.session_state["login_active"]:
    st.title("로그인")
    
    with st.form("login_form"):
        username = st.text_input("아이디 (Username)")
        password = st.text_input("비밀번호 (Password)", type="password")
        
        # 제출 버튼과 취소 버튼
        submitted = st.form_submit_button("로그인")
        cancelled = st.form_submit_button("취소")
        
        if submitted:
            users = load_users_from_yaml()  # 여러 사용자 로드
            
            # 사용자 정보 찾기 (username을 기준)
            user_data = next((user for user in users if user["username"] == username), None)
            
            if user_data:
                if check_password(user_data["password"], password):
                    st.session_state["logged_in"] = True
                    st.session_state["current_user"] = username
                    st.session_state["login_active"] = False
                    st.session_state["registration_active"] = False
                    st.success(f"환영합니다, {user_data['nickname']}님!")
                    st.rerun()  # 로그인 후 자동으로 홈페이지로 이동
                else:
                    st.error("비밀번호가 잘못되었습니다.")
            else:
                st.error("아이디를 찾을 수 없습니다.")
        elif cancelled:
            st.session_state["login_active"] = False  # 로그인 세션 취소


# 세션 상태 초기화 (초기화되지 않은 변수 사용 시 에러 방지)
if "deletion_active" not in st.session_state:
    st.session_state["deletion_active"] = False

# 회원탈퇴 처리
if st.session_state["deletion_active"]:
    st.title("회원탈퇴")
    
    with st.form("deletion_form"):
        password = st.text_input("비밀번호 (Password)", type="password")
        confirm_password = st.text_input("비밀번호 확인 (Confirm Password)", type="password")
        
        # 제출 버튼과 취소 버튼
        submitted = st.form_submit_button("회원탈퇴")
        cancelled = st.form_submit_button("취소")
        
        if submitted:
            users = load_users_from_yaml()  # 여러 사용자 로드
            user_data = next((user for user in users if user["username"] == st.session_state["current_user"]), None)
            
            if user_data:
                if password != confirm_password:
                    st.error("비밀번호가 일치하지 않습니다.")
                elif not check_password(user_data["password"], password):
                    st.error("비밀번호가 올바르지 않거나 일치하지 않습니다.")
                else:
                    # 비밀번호가 맞으면 해당 유저 삭제
                    users = [user for user in users if user["username"] != st.session_state["current_user"]]
                    
                    # 변경된 리스트를 다시 저장
                    save_to_yaml(users)
                    
                    # 세션 초기화 (로그아웃 상태로)
                    st.session_state["logged_in"] = False
                    st.session_state["current_user"] = None
                    st.session_state["deletion_active"] = False
                    st.session_state["login_active"] = False
                    
                    st.success("회원탈퇴가 완료되었습니다.")
                    st.rerun()
            else:
                st.error("회원 정보를 찾을 수 없습니다.")
        elif cancelled:
            st.session_state["deletion_active"] = False #회원탈퇴 세션 취소
            st.rerun()
