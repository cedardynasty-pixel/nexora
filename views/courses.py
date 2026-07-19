import streamlit as st
from style import inject_css, hero, section_title, card

inject_css()

hero(
    "Explore Our Courses",
    "Choose from a wide range of courses designed for students in Grades 6–12. "
    "Every course is carefully structured with lessons, quizzes, notes, and progress tracking.",
)

# ---- SEARCH ----
section_title("Find Your Course", "Search by subject, topic, or grade.")
search_query = st.text_input("Search for a course...", label_visibility="collapsed", placeholder="Search for a course...")

subjects = ["Mathematics", "Science", "English", "Social Science", "Computer Science", "Hindi"]
grades = {
    "Grade 7": "Interactive lessons with practice exercises.",
    "Grade 8": "Build strong concepts for higher grades.",
    "Grade 9": "Comprehensive learning aligned with the latest curriculum.",
    "Grade 10": "Exam-focused preparation with revision resources.",
    "Grade 11": "Advanced concepts for Science, Commerce, and Humanities.",
    "Grade 12": "Comprehensive preparation for board examinations and higher studies.",
}

st.divider()

# ---- BROWSE BY SUBJECT ----
section_title("Browse by Subject", "Select a subject to start learning with interactive lessons and practice materials.")

filtered_subjects = [s for s in subjects if search_query.lower() in s.lower()] if search_query else subjects
if search_query and not filtered_subjects:
    st.info(f"No subjects matching '{search_query}'. Showing all subjects instead.")
    filtered_subjects = subjects

for i in range(0, len(filtered_subjects), 3):
    cols = st.columns(3)
    for col, subj in zip(cols, filtered_subjects[i:i + 3]):
        with col:
            card(subj, "Explore lessons, notes and practice questions.")

st.divider()

# ---- BROWSE BY GRADE ----
section_title("Browse by Grade", "Choose your grade to access courses designed specifically for your level.")

grade_items = list(grades.items())
for i in range(0, len(grade_items), 3):
    cols = st.columns(3)
    for col, (grade, desc) in zip(cols, grade_items[i:i + 3]):
        with col:
            card(grade, desc)

st.divider()

# ---- LEARNING PATHS ----
section_title("Learning Paths", "Choose a structured learning path that matches your academic goals.")

paths = [
    ("Foundation Path",
     "Perfect for students who want to strengthen their understanding of fundamental concepts before moving to advanced topics.",
     ["Step-by-step lessons", "Interactive quizzes", "Progress tracking", "Completion certificate"]),
    ("Exam Preparation",
     "Designed for students preparing for school examinations with revision materials and practice papers.",
     ["Revision notes", "Mock tests", "Previous question papers", "Performance reports"]),
    ("Advanced Learning",
     "Go beyond the classroom with challenging lessons, projects, and higher-level concepts.",
     ["Advanced topics", "Projects", "Skill development", "Achievement badges"]),
]

cols = st.columns(3)
for col, (title, desc, items) in zip(cols, paths):
    with col:
        bullets = "".join(f"<li>{item}</li>" for item in items)
        st.markdown(
            f"""
            <div class="nexora-card">
                <h3>{title}</h3>
                <p>{desc}</p>
                <ul>{bullets}</ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ---- WHY LEARN WITH NEXORA ----
section_title("Why Learn With Nexora?", "Nexora combines modern technology with high-quality education to help students achieve better academic results.")

why = [
    ("Interactive Learning", "Engaging lessons with activities that make difficult concepts easier to understand."),
    ("Expert Resources", "High-quality study materials created to support school learning and exam preparation."),
    ("Anytime Access", "Learn from anywhere using your desktop, tablet, or smartphone."),
]
cols = st.columns(3)
for col, (title, body) in zip(cols, why):
    with col:
        card(title, body)
