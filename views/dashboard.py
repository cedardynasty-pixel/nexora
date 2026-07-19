import streamlit as st
from style import inject_css, hero, section_title
from auth import is_logged_in, current_user, logout, require_login_notice
import db

inject_css()

if not is_logged_in():
    require_login_notice()
    st.stop()

username = current_user()
user = db.get_user(username)

hero(f"Welcome back, {username}! 👋", "Here's a snapshot of your learning progress on Nexora.")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Log Out"):
        logout()
        st.switch_page("views/home.py")

st.divider()

# ---- ACCOUNT INFO ----
section_title("Your Account")
info_cols = st.columns(3)
info_cols[0].metric("Username", user["username"])
info_cols[1].metric("Grade", user["grade"] or "—")
info_cols[2].metric("Member Since", user["created_at"][:10])

st.divider()

# ---- ENROLLED COURSES / PROGRESS ----
section_title("Your Courses", "Track your progress across enrolled subjects.")

enrollments = db.get_enrollments(username)

if not enrollments:
    st.info("You're not enrolled in any subjects yet.")
else:
    for row in enrollments:
        subject, progress = row["subject"], row["progress"]
        st.markdown(f"**{subject}**")
        st.progress(progress / 100, text=f"{progress}% complete")

st.divider()

# ---- ADD / UPDATE A SUBJECT ----
section_title("Update Progress", "Simulate completing lessons in a subject.")

all_subjects = ["Mathematics", "Science", "English", "Social Science", "Computer Science", "Hindi"]
with st.form("progress_form"):
    subject_choice = st.selectbox("Subject", all_subjects)
    new_progress = st.slider("Progress (%)", 0, 100, 10)
    update_submitted = st.form_submit_button("Save Progress")
    if update_submitted:
        db.update_progress(username, subject_choice, new_progress)
        st.success(f"Updated {subject_choice} progress to {new_progress}%.")
        st.rerun()
