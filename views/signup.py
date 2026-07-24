import streamlit as st
from style import inject_css, hero
from auth import login, is_logged_in
import db

inject_css()

if is_logged_in():
    st.success(f"You're already logged in as **{st.session_state['username']}**.")
    st.page_link("views/dashboard.py", label="Go to Dashboard", icon="📊")
    st.stop()

hero("Create Your Free Account", "Join Nexora today and discover a smarter way to learn.")

with st.form("signup_form"):
    username = st.text_input("Choose a username")
    email = st.text_input("Email address")
    grade = st.selectbox("Grade", [f"Grade {g}" for g in range(6, 13)])
    password = st.text_input("Choose a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    submitted = st.form_submit_button("Create Account")

    if submitted:
        if not username.strip() or not email.strip() or not password:
            st.error("Please fill in all fields.")
        elif password != confirm_password:
            st.error("Passwords don't match.")
        elif len(password) < 6:
            st.error("Password should be at least 6 characters.")
        else:
            ok, message = db.create_user(username.strip(), email.strip(), password, grade)
            if ok:
                login(username.strip())
                st.success(message)
                st.switch_page("views/dashboard.py")
            else:
                st.error(message)

st.markdown("Already have an account?")
st.page_link("views/login.py", label="Log in here", icon="🔑")
