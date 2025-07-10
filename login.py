import streamlit as st
from utils.auth import login
from utils.auth import register_user

st.set_page_config(page_title="Question Bank App", layout="centered", initial_sidebar_state='collapsed')

if "user" not in st.session_state:
    st.session_state.user = None

container1 = st.container(border=False)
with container1:
    if st.session_state.user is None:
        container1.title("🔒 Login/Register")
        tab1, tab2 = container1.tabs(['Login', 'Register'], width=700)
        with tab1:
            with st.form("login_form", width=700, height=350):
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

        with tab2:
            with st.form('register-form', width=700, height=350):
                uname = st.text_input(label="", placeholder='Username')
                pwd = st.text_input(label="", type='password', placeholder="Password")
                email = st.text_input(label="", placeholder="Email")
                submitted = st.form_submit_button("Register",
                                                  type="primary")
                if submitted:
                    st.write(submitted, uname, pwd, email)
                    register_user(uname, pwd, email)
                    st.success("Register successfully")

    else:
        st.success(f"✅ Logged in as {st.session_state.user['username']} ({st.session_state.user['role']})")
        if st.button("⏻ Log out", key="local_logout_key"):
            st.session_state.user = None
            st.rerun()


# container2 = st.container(height=50)
# with container2:
#     if not st.user.is_logged_in:
#         st.button("Google Login", on_click=st.login, type="secondary")
#         st.stop()
#     st.write(st.user.items())
#     st.button("Log out", on_click=st.logout)
#     st.markdown(f"Welcome! {st.user.name}")
#
if not st.user.is_logged_in:
    # col_img_m, col_btn_m = st.columns([1, 6], gap=None)
    # with col_img_m:
    #     st.image("microsoft.png", width=32)  # your PNG or SVG
    #
    # with col_btn_m:
    #     st.button(
    #         "Microsoft Login",
    #         on_click=st.login,
    #         type="secondary",
    #         use_container_width=True
    #     )
    st.button("Microsoft Login", on_click=st.login, type="secondary", use_container_width=True)

if not st.user.is_logged_in:
    # col_img_t, col_btn_t = st.columns([1, 6], gap=None)
    # with col_img_t:
    #     st.image("twitter.png", width=32)  # your PNG or SVG
    #
    # with col_btn_t:
    #     st.button(
    #         "Twitter Login",
    #         on_click=st.login,
    #         type="secondary",
    #         use_container_width=True
    #     )
   st.button("Twitter Login", on_click=st.login, type="secondary", use_container_width=True)

if not st.user.is_logged_in:
    # col_img_g, col_btn_g = st.columns([1, 3], gap=None)
    # with col_btn_g:
    #     st.image("google.png", width=32)  # your PNG or SVG
    #
    # with col_btn_g:
    #     st.button(
    #         "Google Login",
    #         on_click=st.login,
    #         type="tertiary",
    #         use_container_width=True
    #     )

    st.button("Google Login", on_click=st.login, type="secondary", use_container_width=True)
    st.stop()
# st.write(st.user.items())

if st.user.is_logged_in:
    st.button("⏻ Log out", on_click=st.logout, key="btn_multi_auth_logout_key")
    st.markdown(f"Welcome! {st.user.name}")

