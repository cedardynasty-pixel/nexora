import streamlit as st
from style import inject_css, hero
from auth import login, is_logged_in
import db

inject_css()

if is_logged_in():
    st.success(f"You're already logged in as **{st.session_state['username']}**.")
    st.page_link("views/dashboard.py", label="Go to Dashboard", icon="📊")
    st.stop()

hero("Welcome Back", "Log in to continue your learning journey with Nexora.")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        ok, message = db.verify_user(username.strip(), password)
        if ok:
            login(username.strip())
            st.success(message)
            st.switch_page("views/dashboard.py")
        else:
            st.error(message)

st.markdown("Don't have an account yet?")
st.page_link("views/signup.py", label="Create one here", icon="✍️")
