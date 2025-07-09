import streamlit as st

def login():
    if "user" not in st.session_state:
        with st.sidebar:
            st.subheader("🔐 Login")
            username = st.text_input("Username")
            if st.button("Login") and username:
                st.session_state["user"] = username
    return st.session_state.get("user")
