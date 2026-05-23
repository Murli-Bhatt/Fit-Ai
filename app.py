import streamlit as st
from services.auth.login import show_login_page
from services.ui.styles import apply_global_styles
from services.persistence.database import init_db
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

# Ensure DB tables exist on every cold start
init_db()

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
        
        # 1. Condition A: Workout Session not active
        if not st.session_state.get("workout_active", False):
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 40px; text-align: center; margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.4);">
                <span style="font-size: 4rem;">⚙️</span>
                <h4 style="color: #ffffff; margin-top: 15px; font-weight: 700; font-size: 1.25rem;">Biometrics Camera Locked</h4>
                <p style="color: #9ca3af; font-weight: 300; max-width: 480px; margin: 10px auto 25px auto; font-size: 0.95rem; line-height: 1.5;">
                    To activate the AI real-time pose tracking coach, please configure your exercise parameters and click the green <b>🚀 Start Workout</b> button in the sidebar.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # 2. Condition B: Workout Session is active
        else:
            exercise_name = st.session_state.active_exercise
            exercise_key = exercise_name.lower().replace(" ", "_").replace("-", "_")
            
            # Segmented toggle for tracking source
            tracking_source = st.radio(
                "Input Modality",
                ["🎥 Live Webcam", "📤 Upload Workout Video"],
                horizontal=True,
                label_visibility="collapsed",
                key="tracking_source"
            )
            
            if tracking_source == "🎥 Live Webcam":
                st.markdown(f"### Live Camera Stream: `{exercise_name}`")
                
                if "camera_active" not in st.session_state:
                    st.session_state.camera_active = False
                    
                if not st.session_state.camera_active:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, rgba(30,41,59,0.3) 0%, rgba(15,23,42,0.5) 100%); border: 1px solid rgba(0, 255, 204, 0.1); border-radius: 20px; padding: 45px 30px; text-align: center; margin-top: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.5);">
                        <span style="font-size: 5rem;">📹</span>
                        <h4 style="color: #ffffff; margin-top: 18px; font-weight: 700; font-size: 1.3rem;">AI Camera Feed Ready</h4>
                        <p style="color: #94a3b8; font-weight: 300; max-width: 460px; margin: 8px auto 28px auto; font-size: 0.95rem; line-height: 1.5;">
                            Your personalized MediaPipe Pose engine is fully configured. Click the button below to initialize the camera stream and start your biomechanics coaching feed.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    if st.button("🎥 Open AI Gym Camera", use_container_width=True, type="primary"):
                        st.session_state.camera_active = True
                        st.rerun()
                else:
                    if st.button("🔌 Shut Down Camera Stream", use_container_width=True, type="secondary"):
                        st.session_state.camera_active = False
                        st.rerun()
                        
                    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                    
                    from streamlit_webrtc import webrtc_streamer, RTCConfiguration
                    from services.vision.pose_processor import PoseVideoProcessor
                    
                    rtc_config = RTCConfiguration(
                        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
                    )
                    
                    ctx = webrtc_streamer(
                        key="pose-tracking-stream",
                        video_processor_factory=lambda: PoseVideoProcessor(exercise_name),
                        rtc_configuration=rtc_config,
                        media_stream_constraints={"video": True, "audio": False},
                    )
                    
                    # Real-time state synchronization bridge between camera frame thread and Streamlit main thread
                    if ctx.video_processor:
                        # Sync angles so sidebar gauges react to movement
                        st.session_state.simulated_angles[exercise_key] = ctx.video_processor.angles
                        
                        # Sync AI coaching cues
                        st.session_state.feedback_cue = ctx.video_processor.feedback
                        
                        # Sync reps completed (triggers SQLite save and full sidebar reload)
                        if ctx.video_processor.new_rep_detected:
                            ctx.video_processor.new_rep_detected = False
                            trigger_rep_success()
                            st.rerun()
            else:
                # 📤 Upload Workout Video Mode
                st.markdown(f"### 📤 Upload Workout Video: `{exercise_name}`")
                
                uploaded_file = st.file_uploader(
                    "Choose an exercise video file...",
                    type=["mp4", "mov", "avi", "mkv"],
                    help="Upload a video showing your exercise from a clear side or front angle."
                )
                
                if uploaded_file is not None:
                    # Temporary save location
                    import os
                    temp_filename = "temp_workout.mp4"
                    
                    # Write file bytes to temp location
                    with open(temp_filename, "wb") as f:
                        f.write(uploaded_file.read())
                        
                    st.success("Video successfully loaded! Ready for AI Biometric Coaching analysis.")
                    
                    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
                    if st.button("⚡ Run AI Biometrics Coach", use_container_width=True, type="primary"):
                        image_placeholder = st.empty()
                        status_placeholder = st.empty()
                        
                        from services.vision.video_processor import process_uploaded_video
                        
                        try:
                            # Run video analysis paced loop
                            reps_done, final_angles = process_uploaded_video(
                                temp_filename,
                                exercise_name,
                                image_placeholder,
                                status_placeholder
                            )
                            
                            # Safely clean up temporary file
                            if os.path.exists(temp_filename):
                                os.remove(temp_filename)
                                
                            # Increment rep success in session history for every completed rep
                            if reps_done > 0:
                                for _ in range(reps_done):
                                    trigger_rep_success()
                                st.success(f"Analysis Complete! Successfully recorded {reps_done} repetitions to active set history.")
                            else:
                                st.warning("Analysis finished. No complete repetitions were detected. Try a clearer video angle!")
                                
                            # Refresh layout so changes propagate to sidebar instantly
                            st.rerun()
                        except Exception as e:
                            import traceback
                            st.error(f"An error occurred during video analysis: {str(e)}")
                            st.code(traceback.format_exc(), language="python")
                            if os.path.exists(temp_filename):
                                os.remove(temp_filename)


    # 3. Workout Logs View
    else:
        st.markdown("<h2 style='color: #ffffff; font-weight: 700;'>📊 Your Logs & Analytical History</h2>", unsafe_allow_html=True)

        from services.persistence.exercise_repository import (
            get_logs_for_user,
            get_exercise_summary,
        )

        user_id = st.session_state.get("user_id")

        # ── All-time logs table ───────────────────────────────────────────────
        db_logs = get_logs_for_user(user_id) if user_id else []

        if not db_logs:
            st.info("No recorded workouts yet! Complete a session in 'Real-Time Tracking' to save your logs.")
            st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.02); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 16px; padding: 30px; text-align: center; margin-top: 20px;">
                <span style="font-size: 3rem;">🔥</span>
                <h4 style="color: #ffffff; margin-top: 10px; font-weight: 600;">Start Your First Streak</h4>
                <p style="color: #9ca3af; font-weight: 300; max-width: 400px; margin: auto; font-size: 0.95rem;">Consistent practice builds muscle memory. Open the tracking space and complete your first set of repetitions!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            # ── Summary cards ─────────────────────────────────────────────────
            summary = get_exercise_summary(user_id)
            if summary:
                st.markdown("### 🏆 All-Time Summary")
                cols = st.columns(min(len(summary), 3))
                for i, row in enumerate(summary):
                    with cols[i % 3]:
                        st.markdown(f"""
                        <div class="stat-card" style="text-align:center; margin-bottom:12px;">
                            <div style="font-size:0.75rem; color:#475569; text-transform:uppercase; letter-spacing:1px;">{row['exercise_name']}</div>
                            <div style="font-size:1.6rem; font-weight:800; color:#00FFCC;">{row['lifetime_reps']}</div>
                            <div style="font-size:0.78rem; color:#94a3b8;">total reps · {row['total_sessions']} sessions</div>
                        </div>
                        """, unsafe_allow_html=True)

            # ── Detailed log table ────────────────────────────────────────────
            st.markdown("### 📋 Session History")
            df = pd.DataFrame([
                {
                    "Date":        row["log_date"],
                    "Exercise":    row["exercise_name"],
                    "Reps Done":   row["total_reps"],
                    "Sets Done":   row["total_sets"],
                    "Target Reps": row["target_reps"],
                    "Target Sets": row["target_sets"],
                    "Last Updated": row["last_updated_at"],
                }
                for row in db_logs
            ])
            st.success(f"Loaded {len(df)} workout records.")
            st.dataframe(df, use_container_width=True)

    # Footer
    st.markdown("""
    <div class="footer">
        FIT-AI Gym Trainer &copy; 2026. Custom Built with Streamlit, SQLite & MediaPipe.
    </div>
    """, unsafe_allow_html=True)
