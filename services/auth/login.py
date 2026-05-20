import streamlit as st
import hashlib
import re
from services.ui.styles import apply_global_styles

# Initialize in-memory database inside Streamlit's Session State
def init_in_memory_db():
    if 'users_db' not in st.session_state:
        # Pre-register a default test account so they can log in instantly
        st.session_state.users_db = {
            "gymcoach": {
                "email": "coach@example.com",
                "password_hash": hashlib.sha256("secure123".encode()).hexdigest()
            }
        }

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Validate email format
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

# Register User (In-Memory)
def register_user(username, email, password):
    init_in_memory_db()
    username_clean = username.strip()
    if username_clean in st.session_state.users_db:
        return False, "Username already exists. Please choose a different one."
    
    st.session_state.users_db[username_clean] = {
        "email": email.strip(),
        "password_hash": hash_password(password)
    }
    return True, "Account created successfully!"

# Authenticate User (In-Memory)
def authenticate_user(username, password):
    init_in_memory_db()
    username_clean = username.strip()
    if username_clean in st.session_state.users_db:
        stored_hash = st.session_state.users_db[username_clean]["password_hash"]
        if stored_hash == hash_password(password):
            return True
    return False

def show_login_page():
    init_in_memory_db()
    
    # Apply unified global styling
    apply_global_styles()
    
    # Initialize Session States for auth tracking
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""
        
    # Central Layout Columns
    col_left, col_mid, col_right = st.columns([1, 2, 1])
    
    with col_mid:
        st.markdown("""
        <div class="login-card">
            <div class="brand-title">🏋️‍♂️ FIT-AI</div>
            <div class="brand-subtitle">Your Intelligent Real-Time Gym Coach</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Simple Tabs for Login and Sign Up
        tab_login, tab_signup = st.tabs(["🔑 LOG IN", "📝 REGISTER"])
        
        with tab_login:
            st.markdown('<div class="form-heading">Sign In</div>', unsafe_allow_html=True)
            
            login_user = st.text_input("Username", key="login_username_field", placeholder="Enter your username")
            login_pass = st.text_input("Password", type="password", key="login_password_field", placeholder="Enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Access Coach Dashboard", key="login_submit_btn", use_container_width=True):
                if not login_user or not login_pass:
                    st.error("Please fill out all fields.")
                else:
                    with st.spinner("Verifying credentials..."):
                        if authenticate_user(login_user, login_pass):
                            st.session_state.logged_in = True
                            st.session_state.username = login_user.strip()
                            st.success(f"Welcome back, {login_user}!")
                            st.rerun()
                        else:
                            st.error("Invalid username or password. Please try again.")
                            
        with tab_signup:
            st.markdown('<div class="form-heading">Create Account</div>', unsafe_allow_html=True)
            
            signup_user = st.text_input("Username", key="signup_username_field", placeholder="Create a unique username")
            signup_email = st.text_input("Email Address", key="signup_email_field", placeholder="name@example.com")
            signup_pass = st.text_input("Choose Password", type="password", key="signup_password_field", placeholder="Must be at least 6 characters")
            signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm_field", placeholder="Re-enter your password")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Create My Account", key="signup_submit_btn", use_container_width=True):
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
                        success, message = register_user(signup_user, signup_email, signup_pass)
                        if success:
                            st.success(message)
                            st.info("You can now switch to the LOG IN tab to sign in!")
                        else:
                            st.error(message)

if __name__ == "__main__":
    show_login_page()
