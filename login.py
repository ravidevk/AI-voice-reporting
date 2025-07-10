import streamlit as st
from utils.auth import login
from utils.auth import register_user

st.set_page_config(page_title="Voice Reporting", layout="centered", initial_sidebar_state='auto')

if "user" not in st.session_state:
    st.session_state.user = None

st.subheader("🔒 SignIn/SignUp")
tab1, tab2 = st.tabs(['SignIn', 'SignUp'], width=500)
with tab1:
    if st.session_state.user is None:
        with st.form("login_form", width=500, height=350):
            username = st.text_input("", placeholder="Username")
            password = st.text_input("", type="password", placeholder="Password")
            submitted = st.form_submit_button("🔑 Login", type="primary")
            if submitted:
                user = login(username, password)
                if user:
                    st.success(f"Welcome {user['username']} ({user['role']})")
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        # multi auth login
        col1, col2, col3 = st.columns(3, border=False)
        if not st.user.is_logged_in:
            col1.button("Github", on_click=st.login, type="secondary", use_container_width=True)

        if not st.user.is_logged_in:
            col2.button("Twitter", on_click=st.login, type="secondary", use_container_width=True)

        if not st.user.is_logged_in:
            col3.button("Google", on_click=st.login, type="secondary", use_container_width=True)
            #st.stop()
        # st.write(st.user.items())

        if st.user.is_logged_in:
            st.button("⏻ Log out", on_click=st.logout, key="btn_multi_auth_logout_key")
            st.markdown(f"Welcome! {st.user.name}")

    else:
        st.success(f"✅ Logged in as {st.session_state.user['username']} ({st.session_state.user['role']})")
        if st.button("⏻ Log out", key="local_logout_key"):
            st.session_state.user = None
            st.rerun()

with tab2:
    with st.form('register-form', clear_on_submit=True):
        uname = st.text_input(label="", placeholder='Username')
        pwd = st.text_input(label="", type='password', placeholder="Password")
        email = st.text_input(label="", placeholder="Role")
        submitted = st.form_submit_button("Register",
                                          type="primary")
        if submitted:
            # st.write(submitted, uname, pwd, email)
            register_user(uname, pwd, email)
            # st.success("Register successfully")





