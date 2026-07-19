import streamlit as st
from style import inject_css, hero, section_title, card, stat
from auth import is_logged_in

inject_css()

hero(
    "Empowering Every Student to Learn Smarter",
    "Nexora is an innovative learning platform designed for students in Grades 6–12. "
    "Explore high-quality lessons, interactive quizzes, AI-powered study tools, and "
    "resources that make learning simple, engaging, and effective.",
)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("See What We Can Do", key="home_see_features"):
        st.session_state["_scroll_features"] = True
with col2:
    if not is_logged_in():
        if st.button("Create Account", key="home_create_account"):
            st.switch_page("views/signup.py")
    else:
        st.page_link("views/dashboard.py", label="Go to Your Dashboard", icon="📊")

st.divider()

# ---- FEATURES ----
section_title("What We Can Do", "Everything you need to learn, revise and succeed in one platform.")

features = [
    ("Interactive Learning", "Study through engaging lessons designed to make every concept easier to understand."),
    ("AI Study Assistant", "Receive instant explanations, summaries and personalized learning support whenever you need it."),
    ("Practice Tests", "Prepare confidently with quizzes and mock examinations based on the latest curriculum."),
    ("Performance Tracking", "Monitor your progress and identify strengths and areas for improvement."),
    ("Digital Notes", "Access organized notes, revision materials and downloadable resources for every subject."),
    ("Available Anytime", "Continue learning from your computer, tablet or smartphone at your convenience."),
]

for i in range(0, len(features), 3):
    cols = st.columns(3)
    for col, (title, body) in zip(cols, features[i:i + 3]):
        with col:
            card(title, body)

st.divider()

# ---- WHY CHOOSE NEXORA ----
section_title("Why Choose Nexora?", "Built to help students achieve better academic results through modern learning experiences.")

why = [
    ("Curriculum Based", "Lessons follow the latest educational curriculum to ensure students stay on track throughout the academic year."),
    ("Expert Content", "Every lesson is designed to be simple, structured and easy to understand."),
    ("Secure Platform", "A safe and reliable learning environment focused on quality education."),
]
cols = st.columns(3)
for col, (title, body) in zip(cols, why):
    with col:
        card(title, body)

st.divider()

# ---- STATS ----
stats = [("10,000+", "Students Learning"), ("500+", "Lessons Available"),
         ("1,000+", "Practice Questions"), ("98%", "Student Satisfaction")]
cols = st.columns(4)
for col, (number, label) in zip(cols, stats):
    with col:
        stat(number, label)

st.divider()

# ---- PLANS ----
section_title("Our Plans", "Choose the learning plan that best fits your educational journey.")

plan_cols = st.columns(3)

with plan_cols[0]:
    st.markdown(
        """
        <div class="nexora-plan">
            <h3>Normal Pack</h3>
            <h1>₹150</h1>
            <ul style="text-align:left;">
                <li>Available for One Month</li>
                <li>Practice quizzes</li>
                <li>Basic progress tracking</li>
                <li>Notes for all Subjects</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Get Started", key="plan_normal"):
        st.switch_page("views/signup.py")

with plan_cols[1]:
    st.markdown(
        """
        <div class="nexora-plan popular">
            <span class="tag">Most Popular</span>
            <h3>Inspire Pack</h3>
            <h1>₹300</h1>
            <ul style="text-align:left;">
                <li>All courses unlocked</li>
                <li>AI Study Assistant</li>
                <li>Unlimited practice tests</li>
                <li>Performance analytics</li>
                <li>Priority support</li>
                <li>Availability for Six Months</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Choose Premium", key="plan_inspire"):
        st.switch_page("views/signup.py")

with plan_cols[2]:
    st.markdown(
        """
        <div class="nexora-plan">
            <h3>Pro Pack</h3>
            <h1>₹800</h1>
            <ul style="text-align:left;">
                <li>Everything in Premium</li>
                <li>Live doubt sessions</li>
                <li>Downloadable study notes</li>
                <li>Exclusive workshops</li>
                <li>Early access to new features</li>
                <li>Availability for One Year</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Go Ultimate", key="plan_pro"):
        st.switch_page("views/signup.py")

st.divider()

# ---- NEWSLETTER ----
section_title("Stay Updated", "Subscribe to receive updates about new features, learning resources and important announcements.")
with st.form("newsletter_form", clear_on_submit=True):
    email = st.text_input("Enter your email address", label_visibility="collapsed", placeholder="Enter your email address")
    submitted = st.form_submit_button("Subscribe")
    if submitted:
        if email and "@" in email:
            st.success("Thanks for subscribing! You'll hear from us soon.")
        else:
            st.error("Please enter a valid email address.")

st.divider()

# ---- CTA ----
st.markdown(
    """
    <div class="nexora-hero" style="text-align:center;">
        <h1>Ready to Begin Your Learning Journey?</h1>
        <p style="margin:auto;">Join Nexora today and discover a smarter way to learn with interactive lessons,
        AI-powered support and personalized progress tracking.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
if not is_logged_in():
    if st.button("Create Your Free Account", key="cta_signup"):
        st.switch_page("views/signup.py")
