import streamlit as st
from services.auth.login import show_login_page
from services.ui.styles import apply_global_styles
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
    # Sidebar Branding
    st.sidebar.markdown("<h2 style='text-align: center; color: #00FFCC; font-weight: 800; margin-bottom: 0px;'>🏋️‍♂️ FIT-AI</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='text-align: center; color: #9ca3af; font-size: 0.95rem; margin-top: 5px;'>Active Coach Session</p>", unsafe_allow_html=True)
    st.sidebar.markdown("---")
    
    st.sidebar.markdown(f"👤 **User:** `{st.session_state.username}`")
    
    # Navigation Selector
    app_mode = st.sidebar.selectbox(
        "Select Workspace",
        ["Welcome Dashboard", "Real-Time Tracking", "Workout Logs & Stats"]
    )
    
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    
    if st.sidebar.button("🔓 Sign Out", use_container_width=True):
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
        
        st.markdown("<h3 style='color: #ffffff; font-weight: 600; margin-bottom: 20px;'>Your AI Gym Pipeline</h3>", unsafe_allow_html=True)
        
        # Grid layout
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class="card">
                <span class="card-icon">📸</span>
                <div class="card-title">Stance & Joint Vision</div>
                <div class="card-desc">Tracks body symmetry and calculates key angles using the 33-point MediaPipe pose landmarker map.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class="card">
                <span class="card-icon">🎙️</span>
                <div class="card-title">LLM Voice Correct</div>
                <div class="card-desc">Translates physical errors into context-sensitive speech cues immediately using Groq & gTTS synthesis.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class="card">
                <span class="card-icon">🗄️</span>
                <div class="card-title">SQLite Session Logs</div>
                <div class="card-desc">Saves and charts total counts, completed set histories, timestamps, and average performance scores.</div>
            </div>
            """, unsafe_allow_html=True)

        # Voice synthesis test tool
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #ffffff; font-weight: 600;'>Test Your Voice Coach</h3>", unsafe_allow_html=True)
        
        col_input, col_action = st.columns([3, 1])
        with col_input:
            user_text = st.text_input("Enter a coaching cue to synthesize:", "Keep your hips back and keep your knees behind your toes.")
        with col_action:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Speak Cue", use_container_width=True):
                from gtts import gTTS
                import io
                
                with st.spinner("Synthesizing audio..."):
                    tts = gTTS(text=user_text, lang='en')
                    fp = io.BytesIO()
                    tts.write_to_fp(fp)
                    fp.seek(0)
                    st.audio(fp, format="audio/mp3")
                    st.success("Voice synthesised!")

    # 2. Real-Time Tracking View
    elif app_mode == "Real-Time Tracking":
        st.markdown("<h2 style='color: #ffffff; font-weight: 700;'>📹 Real-Time Exercise Space</h2>", unsafe_allow_html=True)
        st.write("Configure your active workout, launch your web camera, and start tracking.")
        
        col_setup, col_cam = st.columns([1, 2])
        
        with col_setup:
            st.markdown("### Setup Session")
            exercise = st.selectbox("Exercise Type", ["Squats", "Push-ups", "Bicep Curls"])
            target_reps = st.number_input("Target Reps", min_value=1, max_value=100, value=10)
            voice_coaching = st.toggle("Enable Voice Prompts", value=True)
            
            st.markdown("---")
            st.info("The next step is loading your video feed with MediaPipe tracking overlay. Select 'Start Video' to open your stream.")
            
        with col_cam:
            st.markdown(f"### Live Camera: `{exercise}`")
            st.markdown("""
            <div style="background-color: #1f2937; border: 2px dashed rgba(255, 255, 255, 0.1); border-radius: 12px; height: 350px; display: flex; align-items: center; justify-content: center; flex-direction: column;">
                <span style="font-size: 4rem;">📹</span>
                <p style="color: #9ca3af; margin-top: 10px; font-weight: 300;">WebRTC Camera Feed Initializing...</p>
                <span style="background-color: #00FFCC; color: #090d16; padding: 8px 18px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; cursor: pointer;">
                    Start Video Stream
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
