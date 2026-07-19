import streamlit as st
from style import inject_css, hero, section_title, card, stat

inject_css()

hero(
    "Building the Future of Education",
    "At Nexora, we believe every student deserves access to high-quality education. Our platform "
    "combines technology, interactive learning, and personalized resources to help students from "
    "Grades 6–12 reach their full potential.",
)

# ---- WHO WE ARE ----
section_title(
    "Who We Are",
    "Nexora is a modern educational platform created to make learning simple, engaging, and accessible. "
    "We bring together structured lessons, AI-powered assistance, practice tests, and study resources "
    "into one easy-to-use platform that supports students throughout their academic journey.",
)
cols = st.columns(3)
who_we_are = [
    ("Innovation", "We use modern technology to create smarter learning experiences that help students understand concepts more effectively."),
    ("Accessibility", "Our platform is designed to work seamlessly across desktops, tablets, and smartphones, allowing students to learn anywhere."),
    ("Excellence", "We are committed to providing high-quality educational content that inspires confidence and academic success."),
]
for col, (title, body) in zip(cols, who_we_are):
    with col:
        card(title, body)

st.divider()

# ---- MISSION ----
section_title(
    "Our Mission",
    "Our mission is to make quality education accessible to every student by combining modern "
    "technology, engaging content, and innovative learning tools. We strive to help learners build "
    "confidence, improve academic performance, and develop lifelong learning skills.",
)

st.divider()

# ---- VISION ----
section_title(
    "Our Vision",
    "We envision a future where every student has equal opportunities to succeed through "
    "technology-driven education that is simple, engaging, and available anywhere in the world.",
)
cols = st.columns(3)
vision = [
    ("Global Learning", "Create an educational platform that connects students with high-quality learning resources regardless of location."),
    ("Innovation", "Continuously improve learning experiences through AI, interactive content, and modern educational technologies."),
    ("Student Success", "Empower students with the knowledge, confidence, and skills needed to achieve their academic goals."),
]
for col, (title, body) in zip(cols, vision):
    with col:
        card(title, body)

st.divider()

# ---- CORE VALUES ----
section_title("Our Core Values", "Everything we build at Nexora is guided by our commitment to students and education.")
values = [
    ("Integrity", "We provide reliable, accurate, and trustworthy educational content."),
    ("Innovation", "We embrace creativity and technology to improve learning experiences."),
    ("Inclusivity", "Every learner deserves equal access to quality education regardless of background."),
    ("Excellence", "We continuously improve our platform to deliver the highest learning standards."),
]
for i in range(0, len(values), 2):
    cols = st.columns(2)
    for col, (title, body) in zip(cols, values[i:i + 2]):
        with col:
            card(title, body)

st.divider()

# ---- STATS ----
stats = [("10K+", "Active Students"), ("500+", "Learning Resources"),
         ("1000+", "Practice Questions"), ("98%", "Student Satisfaction")]
cols = st.columns(4)
for col, (number, label) in zip(cols, stats):
    with col:
        stat(number, label)

st.divider()

# ---- TEAM ----
section_title(
    "Meet Our Team",
    "Behind Nexora is a passionate team of educators, developers, designers, and innovators "
    "working together to build a better learning experience for every student.",
)
team = [
    ("Education Experts", "Our academic specialists design structured lessons that align with modern educational standards and help students understand concepts with confidence."),
    ("Technology Team", "Our developers create a fast, secure, and user-friendly platform that makes learning simple across all devices."),
    ("Support Team", "Our dedicated support staff is always ready to assist students and ensure a smooth learning experience."),
]
cols = st.columns(3)
for col, (title, body) in zip(cols, team):
    with col:
        card(title, body)

st.divider()

# ---- CTA ----
st.markdown(
    """
    <div class="nexora-hero" style="text-align:center;">
        <h1>Become a Part of Nexora</h1>
        <p style="margin:auto;">Join thousands of students who are already learning smarter with Nexora.
        Start your journey today and unlock your full academic potential.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
if st.button("Create Your Free Account", key="about_cta_signup"):
    st.switch_page("views/signup.py")
