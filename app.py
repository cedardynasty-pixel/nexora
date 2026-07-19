"""
app.py — Nexora Streamlit app entry point.

Run with:  streamlit run app.py
"""

import streamlit as st
import db
from auth import is_logged_in, current_user

st.set_page_config(page_title="Nexora | Learn Without Limits", page_icon="🎓", layout="wide")

db.init_db()

# ---- Sidebar branding ----
with st.sidebar:
    st.markdown("## 🎓 NEXORA")
    if is_logged_in():
        st.caption(f"Logged in as **{current_user()}**")
    else:
        st.caption("Learn Without Limits")

# ---- Build navigation (Dashboard only shown once logged in) ----
home_page = st.Page("views/home.py", title="Home", icon="🏠", default=True)
courses_page = st.Page("views/courses.py", title="Courses", icon="📚")
about_page = st.Page("views/about.py", title="About", icon="ℹ️")

if is_logged_in():
    login_page = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
    account_pages = [login_page]
else:
    login_page = st.Page("views/login.py", title="Login", icon="🔑")
    signup_page = st.Page("views/signup.py", title="Sign Up", icon="✍️")
    account_pages = [login_page, signup_page]

pg = st.navigation(
    {
        "Explore": [home_page, courses_page, about_page],
        "Account": account_pages,
    }
)
pg.run()
