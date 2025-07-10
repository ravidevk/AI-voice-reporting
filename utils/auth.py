import streamlit as st
import json

# def login():
#     if "user" not in st.session_state:
#         with st.sidebar:
#             st.subheader("🔐 Login")
#             username = st.text_input("Username")
#             if st.button("Login") and username:
#                 st.session_state["user"] = username
#     return st.session_state.get("user")


def load_users():
    with open("user.json") as f:
        return json.load(f)


# save user to json
def save_users(user):
    with open("user.json", "w") as f:
        json.dump(user, f, indent=4)


def login(username, password):
    users = load_users()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return user
    return None


def require_role(allowed_roles):
    user = st.session_state.get("user")
    if st.user.is_logged_in:
        return False
    elif user and user["role"] in allowed_roles:
        return True
    else:
        st.error("Unauthorized access")
        st.stop()


# Register a new user
def register_user(username, password, role):
    st.write(username, password, role)
    users = load_users()

    # Check for existing username
    for user in users:
        if user["username"] == username:
            st.warning("Username already exists.")
            return False

    users.append({
        "username": username,
        "password": password,
        "role": role
    })

    save_users(users)
    st.success("User registered successfully.")
    return True
