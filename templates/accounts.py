import streamlit as st
import requests

# Function to display the login page
def login_page():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Sending login request to Django API
        url = "http://127.0.0.1:8000//accounts/login/"
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)
        
        if response.status_code == 200:
            st.success("로그인 성공!")
            user_data = response.json().get("user")
            st.write("User Data:", user_data)
            # Store login status in session state
            st.session_state.logged_in = True
        else:
            st.error(response.json().get("message"))

# Function to display the logout page
def logout_page():
    st.title("Logout")
    
    if st.button("Logout"):
        # Sending logout request to Django API
        url = "http://127.0.0.1:8000/accounts/logout/"
        response = requests.post(url)
        
        if response.status_code == 200:
            st.success("로그아웃 성공!")
            # Reset session state
            st.session_state.logged_in = False
        else:
            st.error("로그아웃 실패")


# Streamlit form to take user inputs for signup
def signup_page():
    st.title("Sign Up")
    
    full_name = st.text_input("Full Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")
    
    if st.button("Sign Up"):
        # Sending signup request to Django API
        url = "http://127.0.0.1:8000/accounts/signup/"  # Django 백엔드의 URL로 수정
        data = {
            "full_name": full_name,
            "username": username,
            "password": password,
            "confirm_password": confirm_password,
        }
        response = requests.post(url, data=data)
        
        if response.status_code == 201:
            st.success("회원가입 성공!")
            user_data = response.json().get("user")
            st.write("User Data:", user_data)
        else:
            st.error(response.json().get("detail"))



def main():
    st.sidebar.title("App Navigation")
    app_mode = st.sidebar.radio("Choose an action", ["Sign Up", "Login"])
    
    if app_mode == "Sign Up":
        signup_page()
    elif app_mode == "Login":
        login_page()

if __name__ == "__main__":
    main()