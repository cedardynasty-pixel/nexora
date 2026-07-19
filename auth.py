"""
auth.py — thin wrapper around st.session_state for login/logout state.
"""

import streamlit as st


def is_logged_in() -> bool:
    return st.session_state.get("username") is not None


def current_user() -> str | None:
    return st.session_state.get("username")


def login(username: str):
    st.session_state["username"] = username


def logout():
    st.session_state.pop("username", None)


def require_login_notice():
    """Show a friendly notice when a protected page is hit while logged out."""
    st.warning("You need to log in to view this page.")
    st.page_link("views/login.py", label="Go to Login", icon="🔑")
