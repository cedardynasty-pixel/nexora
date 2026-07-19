"""
style.py — shared CSS for the Nexora Streamlit app.

The original site's css/js/images folders were not included in the upload,
so this recreates a clean, modern edtech look natively for Streamlit
rather than porting nonexistent files.
"""

import streamlit as st

NEXORA_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

:root {
    --nexora-primary: #6C5CE7;
    --nexora-primary-dark: #4834d4;
    --nexora-accent: #00cec9;
    --nexora-bg-soft: #f5f4ff;
}

/* Hero banner */
.nexora-hero {
    background: linear-gradient(135deg, var(--nexora-primary) 0%, var(--nexora-primary-dark) 100%);
    color: white;
    padding: 3rem 2.5rem;
    border-radius: 20px;
    margin-bottom: 2rem;
}
.nexora-hero h1 {
    color: white;
    font-size: 2.3rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.nexora-hero p {
    color: #e8e6ff;
    font-size: 1.05rem;
    max-width: 700px;
}

/* Generic content card */
.nexora-card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 2px 12px rgba(108, 92, 231, 0.10);
    border: 1px solid #eee6ff;
    height: 100%;
    margin-bottom: 1rem;
}
.nexora-card h3 {
    color: var(--nexora-primary-dark);
    margin-top: 0;
}

/* Stat boxes */
.nexora-stat {
    text-align: center;
    background: var(--nexora-bg-soft);
    border-radius: 14px;
    padding: 1.2rem 0.5rem;
    margin-bottom: 1rem;
}
.nexora-stat h2 {
    color: var(--nexora-primary);
    font-size: 1.9rem;
    margin-bottom: 0.2rem;
}
.nexora-stat p {
    color: #555;
    margin: 0;
}

/* Pricing card */
.nexora-plan {
    background: white;
    border-radius: 18px;
    padding: 1.6rem;
    text-align: center;
    border: 2px solid #eee6ff;
    height: 100%;
}
.nexora-plan.popular {
    border-color: var(--nexora-primary);
    box-shadow: 0 4px 20px rgba(108, 92, 231, 0.25);
}
.nexora-plan .tag {
    background: var(--nexora-primary);
    color: white;
    font-size: 0.75rem;
    padding: 0.2rem 0.7rem;
    border-radius: 20px;
    display: inline-block;
    margin-bottom: 0.5rem;
}
.nexora-plan h1 {
    color: var(--nexora-primary-dark);
    font-size: 2rem;
    margin: 0.3rem 0;
}

/* Section title */
.nexora-section-title h2 {
    font-weight: 700;
    margin-bottom: 0.2rem;
}
.nexora-section-title p {
    color: #666;
}

/* Buttons: recolor Streamlit's default button to match brand */
div.stButton > button {
    background: var(--nexora-primary);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.5rem 1.2rem;
    font-weight: 600;
}
div.stButton > button:hover {
    background: var(--nexora-primary-dark);
    color: white;
}

/* Sidebar branding */
[data-testid="stSidebarNav"] ul {
    padding-top: 0.5rem;
}
</style>
"""


def inject_css():
    st.markdown(NEXORA_CSS, unsafe_allow_html=True)


def hero(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="nexora-hero">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="nexora-section-title">
            <h2>{title}</h2>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def card(title: str, body: str):
    st.markdown(
        f"""
        <div class="nexora-card">
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat(number: str, label: str):
    st.markdown(
        f"""
        <div class="nexora-stat">
            <h2>{number}</h2>
            <p>{label}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
