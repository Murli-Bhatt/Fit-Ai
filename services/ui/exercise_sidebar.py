import streamlit as st
from services.state.session import (
    init_workout_session,
    start_workout_session,
    stop_workout_session
)
from services.ui.metrics.progress import render_progress_metric
from services.ui.metrics.squats import render_squat_metrics
from services.ui.metrics.pushups import render_pushup_metrics
from services.ui.metrics.bicep_curls import render_bicep_curl_metrics
from services.ui.metrics.plank import render_plank_metrics
from services.ui.metrics.lunges import render_lunge_metrics
from services.ui.metrics.shoulder_press import render_shoulder_press_metrics

def render_exercise_sidebar():
    """
    Renders the custom, premium workout sidebar that switches modes.
    Ensures safe initialization, edge-case checks, and calls correct widgets.
    """
    # 1. Ensure all session states are safely initialized
    init_workout_session()
    
    # 2. Render Inactive View: Setup Configurator
    if not st.session_state.workout_active:
        st.sidebar.markdown("<div class='form-heading'>⚙️ Setup Session</div>", unsafe_allow_html=True)

        exercise_list = [
            "Squats",
            "Push-ups",
            "Bicep Curls",
            "Plank",
            "Lunges",
            "Shoulder Press"
        ]

        # Safeguard index boundaries when fetching from session state
        try:
            default_idx = exercise_list.index(st.session_state.active_exercise)
        except ValueError:
            default_idx = 0

        st.sidebar.selectbox(
            "Exercise Type",
            exercise_list,
            index=default_idx,
            key="widget_active_exercise"
        )

        col1, col2 = st.sidebar.columns(2)
        with col1:
            st.number_input(
                "Sets", 
                min_value=1, 
                max_value=8, 
                value=int(st.session_state.target_sets),
                step=1, 
                key="widget_target_sets"
            )
        with col2:
            st.number_input(
                "Reps / Set", 
                min_value=1, 
                max_value=30, 
                value=int(st.session_state.target_reps),
                step=1, 
                key="widget_target_reps"
            )

        st.sidebar.toggle(
            "🎙️ Voice Coaching", 
            value=bool(st.session_state.voice_coaching),
            key="widget_voice_coaching"
        )

        st.sidebar.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        if st.sidebar.button("🚀 Start Workout", use_container_width=True, type="primary"):
            start_workout_session(
                exercise=st.session_state.widget_active_exercise,
                sets=st.session_state.widget_target_sets,
                reps=st.session_state.widget_target_reps,
                voice_coaching=st.session_state.widget_voice_coaching
            )
            st.rerun()
            
    # 3. Render Active View: Real-Time Performance Analytics
    else:
        # Display Glowing Active Workout Header
        st.sidebar.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 255, 204, 0.1) 0%, rgba(0, 153, 255, 0.1) 100%); border: 1px solid rgba(0, 255, 204, 0.3); border-radius: 12px; padding: 12px; text-align: center; margin-bottom: 12px;">
            <div style="font-size: 0.75rem; color: #00FFCC; font-weight: 800; text-transform: uppercase; letter-spacing: 1.5px;">Active Workout</div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff; margin-top: 3px;">{st.session_state.active_exercise}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time toggle to enable/disable voice coaching during session
        active_voice = st.sidebar.toggle(
            "🎙️ Voice Coaching", 
            value=bool(st.session_state.voice_coaching),
            key="widget_active_voice_coaching"
        )
        st.session_state.voice_coaching = active_voice
        
        # A. Progress Metric Card Placeholder
        st.session_state.progress_placeholder = st.sidebar.empty()
        with st.session_state.progress_placeholder.container():
            render_progress_metric(
                st.session_state.set_history, 
                st.session_state.current_set, 
                st.session_state.current_reps, 
                st.session_state.target_reps
            )
        st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 15px 0;'>", unsafe_allow_html=True)
        
        # B. Load Specific Posture Metrics Widget Placeholder
        exercise_key = st.session_state.active_exercise.lower().replace(" ", "_").replace("-", "_")
        angles = st.session_state.simulated_angles.get(exercise_key, {})
        
        st.session_state.metrics_placeholder = st.sidebar.empty()
        with st.session_state.metrics_placeholder.container():
            render_exercise_metrics(st.session_state.active_exercise, angles)
                
        st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 15px 0;'>", unsafe_allow_html=True)
        
        # C. Coaching Voice Cue Bubble Placeholder
        st.session_state.feedback_placeholder = st.sidebar.empty()
        with st.session_state.feedback_placeholder.container():
            st.markdown(f"""
            <div class="speech-box">
                <span style="font-size: 0.95rem; font-weight: 700; color: #00FFCC; display: flex; align-items: center; gap: 6px;">
                    🎙️ AI Coach Cue
                </span>
                <p style="color: #cbd5e1; font-size: 0.85rem; font-weight: 300; margin: 6px 0 0 0; line-height: 1.4;">
                    "{st.session_state.feedback_cue}"
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.sidebar.markdown("<hr style='border-color: rgba(255,255,255,0.06); margin: 15px 0;'>", unsafe_allow_html=True)
        
        # D. Developer Simulator Expander (For Manual Testing & Validation inside Sidebar)
        with st.sidebar.expander("🧪 Developer Simulator", expanded=False):
            st.markdown("<p style='font-size: 0.8rem; color: #9ca3af;'>Adjust joint angles to simulate postural feedback:</p>", unsafe_allow_html=True)
            
            exercise_name = st.session_state.active_exercise
            if exercise_name == "Squats":
                knee_val = st.slider("Knee Flexion Angle", min_value=40.0, max_value=180.0, value=float(st.session_state.simulated_angles["squats"]["knee"]), step=1.0)
                hip_val = st.slider("Hip Flexion Angle", min_value=40.0, max_value=180.0, value=float(st.session_state.simulated_angles["squats"]["hip"]), step=1.0)
                st.session_state.simulated_angles["squats"]["knee"] = knee_val
                st.session_state.simulated_angles["squats"]["hip"] = hip_val
                
            elif exercise_name == "Push-ups":
                elbow_val = st.slider("Elbow Flexion Angle", min_value=40.0, max_value=180.0, value=float(st.session_state.simulated_angles["push_ups"]["elbow"]), step=1.0)
                torso_val = st.slider("Torso Alignment Angle", min_value=130.0, max_value=200.0, value=float(st.session_state.simulated_angles["push_ups"]["torso"]), step=1.0)
                st.session_state.simulated_angles["push_ups"]["elbow"] = elbow_val
                st.session_state.simulated_angles["push_ups"]["torso"] = torso_val
                
            elif exercise_name == "Bicep Curls":
                elbow_l_val = st.slider("Left Elbow Angle", min_value=30.0, max_value=180.0, value=float(st.session_state.simulated_angles["bicep_curls"]["elbow_l"]), step=1.0)
                elbow_r_val = st.slider("Right Elbow Angle", min_value=30.0, max_value=180.0, value=float(st.session_state.simulated_angles["bicep_curls"]["elbow_r"]), step=1.0)
                stability_val = st.selectbox("Upper Arm Stability", ["High", "Medium", "Low"], index=["High", "Medium", "Low"].index(st.session_state.simulated_angles["bicep_curls"]["stability"]))
                st.session_state.simulated_angles["bicep_curls"]["elbow_l"] = elbow_l_val
                st.session_state.simulated_angles["bicep_curls"]["elbow_r"] = elbow_r_val
                st.session_state.simulated_angles["bicep_curls"]["stability"] = stability_val
                
            elif exercise_name == "Plank":
                hip_val = st.slider("Hip Alignment Angle", min_value=130.0, max_value=200.0, value=float(st.session_state.simulated_angles["plank"]["hip"]), step=1.0)
                elbow_val = st.slider("Elbow Stacked Angle", min_value=60.0, max_value=120.0, value=float(st.session_state.simulated_angles["plank"]["elbow"]), step=1.0)
                st.session_state.simulated_angles["plank"]["hip"] = hip_val
                st.session_state.simulated_angles["plank"]["elbow"] = elbow_val
                
            elif exercise_name == "Lunges":
                fknee_val = st.slider("Lead Front Knee Angle", min_value=40.0, max_value=180.0, value=float(st.session_state.simulated_angles["lunges"]["front_knee"]), step=1.0)
                bknee_val = st.slider("Rear Back Knee Angle", min_value=40.0, max_value=180.0, value=float(st.session_state.simulated_angles["lunges"]["back_knee"]), step=1.0)
                st.session_state.simulated_angles["lunges"]["front_knee"] = fknee_val
                st.session_state.simulated_angles["lunges"]["back_knee"] = bknee_val
                
            elif exercise_name == "Shoulder Press":
                elbow_l_val = st.slider("Left Elbow Angle", min_value=30.0, max_value=180.0, value=float(st.session_state.simulated_angles["shoulder_press"]["elbow_l"]), step=1.0)
                elbow_r_val = st.slider("Right Elbow Angle", min_value=30.0, max_value=180.0, value=float(st.session_state.simulated_angles["shoulder_press"]["elbow_r"]), step=1.0)
                st.session_state.simulated_angles["shoulder_press"]["elbow_l"] = elbow_l_val
                st.session_state.simulated_angles["shoulder_press"]["elbow_r"] = elbow_r_val
                
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔥 Simulate Completed Repetition", use_container_width=True, type="primary"):
                from services.state.session import trigger_rep_success
                trigger_rep_success()
                st.toast(st.session_state.feedback_cue, icon="🏋️‍♂️")
                st.rerun()
                
        st.sidebar.markdown("<br>", unsafe_allow_html=True)
        
        # E. Session Actions (Stop / Finish Workout)
        if st.sidebar.button("🛑 Finish / Stop Session", use_container_width=True, type="secondary"):
            stop_workout_session()
            st.success("Session completed and saved.")
            st.rerun()

def render_exercise_metrics(exercise_name, angles):
    """
    Utility to map specific exercises to their rendering methods.
    """
    if exercise_name == "Squats":
        render_squat_metrics(angles)
    elif exercise_name == "Push-ups":
        render_pushup_metrics(angles)
    elif exercise_name == "Bicep Curls":
        render_bicep_curl_metrics(angles)
    elif exercise_name == "Plank":
        render_plank_metrics(angles)
    elif exercise_name == "Lunges":
        render_lunge_metrics(angles)
    elif exercise_name == "Shoulder Press":
        render_shoulder_press_metrics(angles)
