"""
login.py
--------
Authentication UI and logic for FIT-AI Gym Trainer.
All user data is now persisted in SQLite via user_repository.
"""

import re
import streamlit as st
from services.ui.styles import apply_global_styles
from services.persistence.database import init_db
from services.persistence.user_repository import (
    register_user,
    authenticate_user,
)


def is_valid_email(email: str) -> bool:
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def show_login_page():
    # Ensure DB and tables exist before any auth operation
    init_db()

    apply_global_styles()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

    _, col_mid, _ = st.columns([1, 2, 1])

    with col_mid:
        st.markdown("""
        <div class="login-card">
            <div class="brand-title">🏋️‍♂️ FIT-AI</div>
            <div class="brand-subtitle">Your Intelligent Real-Time Gym Coach</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs(["🔑 LOG IN", "📝 REGISTER"])

        # ── LOGIN ─────────────────────────────────────────────────────────────
        with tab_login:
            st.markdown('<div class="form-heading">Sign In</div>', unsafe_allow_html=True)

            login_user = st.text_input(
                "Username", key="login_username_field",
                placeholder="Enter your username"
            )
            login_pass = st.text_input(
                "Password", type="password", key="login_password_field",
                placeholder="Enter your password"
            )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Access Coach Dashboard", key="login_submit_btn",
                         use_container_width=True, type="primary"):
                if not login_user or not login_pass:
                    st.error("Please fill out all fields.")
                else:
                    with st.spinner("Verifying credentials..."):
                        success, user_id = authenticate_user(login_user, login_pass)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username  = login_user.strip()
                            st.session_state.user_id   = user_id
                            st.success(f"Welcome back, {login_user}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password. Please try again.")

        # ── REGISTER ──────────────────────────────────────────────────────────
        with tab_signup:
            st.markdown('<div class="form-heading">Create Account</div>', unsafe_allow_html=True)

            signup_user    = st.text_input(
                "Username", key="signup_username_field",
                placeholder="Create a unique username"
            )
            signup_email   = st.text_input(
                "Email Address", key="signup_email_field",
                placeholder="name@example.com"
            )
            signup_pass    = st.text_input(
                "Choose Password", type="password", key="signup_password_field",
                placeholder="Must be at least 6 characters"
            )
            signup_confirm = st.text_input(
                "Confirm Password", type="password", key="signup_confirm_field",
                placeholder="Re-enter your password"
            )

            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create My Account", key="signup_submit_btn",
                         use_container_width=True, type="primary"):
                if not signup_user or not signup_email or not signup_pass or not signup_confirm:
                    st.error("Please fill out all fields.")
                elif signup_pass != signup_confirm:
                    st.error("Passwords do not match.")
                elif not is_valid_email(signup_email):
                    st.error("Please enter a valid email address.")
                elif len(signup_pass) < 6:
                    st.error("Password must be at least 6 characters long.")
                else:
                    with st.spinner("Creating your profile..."):
                        ok, message = register_user(signup_user, signup_email, signup_pass)
                        if ok:
                            st.success(message)
                            st.info("You can now switch to the LOG IN tab to sign in!")
                        else:
                            st.error(message)


if __name__ == "__main__":
    show_login_page()
