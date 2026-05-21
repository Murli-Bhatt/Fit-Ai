import streamlit as st
from services.auth.login import show_login_page
from services.ui.styles import apply_global_styles
from services.state.session import init_workout_session, trigger_rep_success
from services.ui.exercise_sidebar import render_exercise_sidebar
import pandas as pd

# Page config
st.set_page_config(
    page_title="AI Gym Trainer",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global premium styling
apply_global_styles()

# Main Application Router
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    show_login_page()
else:
    # Ensure active session state is safely loaded
    init_workout_session()
    
    # ── Sidebar Branding ──
    st.sidebar.markdown(f"""
    <div style="text-align:center; padding: 8px 0 12px 0;">
        <div style="font-size:1.6rem; font-weight:800; background:linear-gradient(135deg,#00FFCC,#0099FF);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent; letter-spacing:2px;">
            🏋️ FIT-AI
        </div>
        <div style="font-size:0.72rem; color:#475569; font-weight:500;
                    text-transform:uppercase; letter-spacing:1.5px; margin-top:3px;">
            AI Gym Coach
        </div>
    </div>
    <div style="background:rgba(0,255,204,0.05); border:1px solid rgba(0,255,204,0.12);
                border-radius:8px; padding:8px 12px; margin-bottom:14px;
                display:flex; align-items:center; gap:8px;">
        <span style="font-size:1rem;">👤</span>
        <div>
            <div style="font-size:0.7rem; color:#475569; text-transform:uppercase; letter-spacing:0.8px;">Logged in as</div>
            <div style="font-size:0.88rem; color:#00FFCC; font-weight:700;">{st.session_state.username}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Navigation Selector ──
    app_mode = st.sidebar.selectbox(
        "Workspace",
        ["Welcome Dashboard", "Real-Time Tracking", "Workout Logs & Stats"],
        label_visibility="collapsed"
    )
    
    # Render exercise sidebar if tracking mode is active
    if app_mode == "Real-Time Tracking":
        st.sidebar.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin:10px 0;'>", unsafe_allow_html=True)
        render_exercise_sidebar()

    st.sidebar.markdown("<hr style='border-color:rgba(255,255,255,0.06); margin:10px 0;'>", unsafe_allow_html=True)
    if st.sidebar.button("🔓 Sign Out", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Successfully logged out.")
        st.rerun()

    # 1. Welcome Dashboard View
    if app_mode == "Welcome Dashboard":
        st.markdown(f"""
        <div class="hero-container">
            <div class="hero-title">WELCOME BACK, {st.session_state.username.upper()}!</div>
            <div class="hero-subtitle">Your personal AI camera trainer is initialized and ready to correct your posture.</div>
            <p style="color: #6b7280; font-size: 0.9rem; font-weight: 300;">Ready to crush your workout today? Select "Real-Time Tracking" from the sidebar.</p>
        </div>
        """, unsafe_allow_html=True)

    # 2. Real-Time Tracking View
    elif app_mode == "Real-Time Tracking":
        st.markdown("<h2 style='color: #ffffff; font-weight: 700;'>📹 Real-Time Biomechanical Arena</h2>", unsafe_allow_html=True)
        st.write("Configure your active session and view real-time posture feeds.")
        
        # Display the live camera placeholder stream
        exercise_name = st.session_state.active_exercise
        st.markdown(f"### Live Camera Stream: `{exercise_name}`")
        st.markdown(f"""
        <div style="background-color: #1f2937; border: 2px dashed rgba(255, 255, 255, 0.1); border-radius: 16px; height: 420px; display: flex; align-items: center; justify-content: center; flex-direction: column; box-shadow: inset 0 4px 30px rgba(0, 0, 0, 0.5);">
            <span style="font-size: 5rem;">📹</span>
            <p style="color: #9ca3af; margin-top: 15px; font-weight: 300; font-size: 1.1rem;">MediaPipe WebRTC Camera Feed Initializing...</p>
            <span style="background-color: #00FFCC; color: #090d16; padding: 12px 28px; border-radius: 20px; font-weight: 600; font-size: 0.95rem; cursor: pointer; box-shadow: 0 4px 20px rgba(0, 255, 204, 0.3); transition: transform 0.2s;">
                Start Video Feed
            </span>
        </div>
        """, unsafe_allow_html=True)

    # 3. Workout Logs View
    else:
        st.markdown("<h2 style='color: #ffffff; font-weight: 700;'>📊 Your Logs & Analytical History</h2>", unsafe_allow_html=True)
        
        # Initialize in-memory logs if they do not exist
        if 'workout_logs' not in st.session_state:
            st.session_state.workout_logs = []
            
        # Filter in-memory logs for current user
        user_logs = [
            {
                "Exercise": log["exercise"],
                "Completed Reps": log["reps"],
                "Timestamp": log["timestamp"]
            }
            for log in st.session_state.workout_logs
            if log["username"] == st.session_state.username
        ]
        
        if not user_logs:
            st.info("No recorded workouts yet! Complete a session in 'Real-Time Tracking' to save your logs.")
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 30px; text-align: center; margin-top: 20px;">
                <span style="font-size: 3rem;">🔥</span>
                <h4 style="color: #ffffff; margin-top: 10px; font-weight: 600;">Start Your First Streak</h4>
                <p style="color: #9ca3af; font-weight: 300; max-width: 400px; margin: auto; font-size: 0.95rem;">Consistent practice builds muscle memory. Open the tracking space and complete your first set of repetitions!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            df = pd.DataFrame(user_logs)
            st.success(f"Loaded {len(df)} workout history records!")
            st.dataframe(df, use_container_width=True)

    # Footer
    st.markdown("""
    <div class="footer">
        FIT-AI Gym Trainer &copy; 2026. Custom Built with Streamlit, SQLite & MediaPipe.
    </div>
    """, unsafe_allow_html=True)
