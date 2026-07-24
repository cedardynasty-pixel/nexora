"""
app.py — Nexora Streamlit app entry point.

Run with:  streamlit run app.py
"""

import streamlit as st
import db
from auth import is_logged_in, current_user, is_admin

st.set_page_config(page_title="Nexora | Learn Without Limits", page_icon="🎓", layout="wide")

db.init_db()

# Create a first admin account if none exists yet. Override the defaults via
# Streamlit secrets (Settings -> Secrets) with ADMIN_USERNAME / ADMIN_EMAIL / ADMIN_PASSWORD.
db.seed_default_admin(
    username=st.secrets.get("ADMIN_USERNAME", "admin"),
    email=st.secrets.get("ADMIN_EMAIL", "admin@nexora.local"),
    password=st.secrets.get("ADMIN_PASSWORD", "changeme123"),
)

# ---- Sidebar branding ----
with st.sidebar:
    st.markdown("## 🎓 NEXORA")
    if is_logged_in():
        st.caption(f"Logged in as **{current_user()}**")
    else:
        st.caption("Learn Without Limits")

# ---- Build navigation ----
# IMPORTANT: pages that are ever targeted by st.switch_page() must always be
# registered here, regardless of login state — Streamlit only allows
# switch_page() to a page that exists in the CURRENT run's navigation. Access
# control for these pages is handled inside each page file instead (they
# check is_logged_in()/is_admin() themselves and show a notice if blocked).
home_page = st.Page("views/home.py", title="Home", icon="🏠", default=True)
courses_page = st.Page("views/courses.py", title="Courses", icon="📚")
about_page = st.Page("views/about.py", title="About", icon="ℹ️")
dashboard_page = st.Page("views/dashboard.py", title="Dashboard", icon="📊")
ai_tools_page = st.Page("views/ai_tools.py", title="AI Study Tools", icon="🤖")
login_page = st.Page("views/login.py", title="Login", icon="🔑")
signup_page = st.Page("views/signup.py", title="Sign Up", icon="✍️")

explore_pages = [home_page, courses_page, about_page]

if is_logged_in():
    if is_admin():
        admin_page = st.Page("views/admin.py", title="Admin Panel", icon="🛡️")
        account_pages = [dashboard_page, admin_page]
    else:
        account_pages = [dashboard_page, ai_tools_page]
else:
    account_pages = [login_page, signup_page]
    # Still registered so switch_page("views/dashboard.py") after a successful
    # login (before this run's nav was built) doesn't raise — they'll just see
    # the "please log in" notice if they land here some other way pre-login.
    account_pages += [dashboard_page, ai_tools_page]

pg = st.navigation(
    {
        "Explore": explore_pages,
        "Account": account_pages,
    }
)
pg.run()
