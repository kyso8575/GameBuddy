import streamlit as st


st.title("챗봇")
st.write("chatbot")

def chatbot():
    st.title("챗봇2")
    st.write("chatbot2")

    if st.session_state["logged_in"]:
        st.write("로그인된 상태")
    else:
        st.write("로그인되지않음")