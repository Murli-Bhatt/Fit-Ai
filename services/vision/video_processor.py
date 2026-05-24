import cv2
import os
import time
import numpy as np
import streamlit as st
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Import modular detectors
from detectors.squat_detector import SquatDetector
from detectors.pushup_detector import PushupDetector
from detectors.bicep_curl_detector import BicepCurlDetector
from detectors.plank_detector import PlankDetector
from detectors.lunge_detector import LungeDetector
from detectors.shoulder_press_detector import ShoulderPressDetector

def process_uploaded_video(file_path, exercise_name, image_placeholder, status_placeholder, audio_placeholder):
    """
    Parses a recorded workout video frame-by-frame, runs posture biometrics
    using MediaPipe Pose Landmarker (VIDEO mode), overlays pose skeletons/HUDs,
    and streams them to the Streamlit canvas at native frame rates.
    
    Returns:
        total_reps (int): total repetitions completed
        final_angles (dict): final joint angles/biometrics state
    """
    # 1. Initialize selected exercise detector from session state to preserve progress
    if "video_detector" in st.session_state and st.session_state.video_detector is not None:
        detector = st.session_state.video_detector
        prev_reps = st.session_state.get("video_prev_reps", 0)
        exercise_key = exercise_name.lower().replace(" ", "_").replace("-", "_")
        final_angles = st.session_state.simulated_angles.get(exercise_key, {})
    else:
        prev_reps = 0
        if exercise_name == "Squats":
            detector = SquatDetector()
            final_angles = {"knee": 170.0, "hip": 170.0, "depth": "Standing", "back": "Neutral Spine"}
        elif exercise_name == "Push-ups":
            detector = PushupDetector()
            final_angles = {"elbow": 175.0, "torso": 178.0, "depth": "Top Plank", "symmetry": "Balanced"}
        elif exercise_name == "Bicep Curls":
            detector = BicepCurlDetector()
            final_angles = {"elbow_l": 165.0, "elbow_r": 165.0, "stability": "High", "range": "Full Extension"}
        elif exercise_name == "Plank":
            detector = PlankDetector()
            final_angles = {"hip": 178.0, "elbow": 90.0, "stability": "Optimal", "duration": 0}
        elif exercise_name == "Lunges":
            detector = LungeDetector()
            final_angles = {"front_knee": 170.0, "back_knee": 165.0, "torso": "Straight", "depth": "Standing"}
        elif exercise_name == "Shoulder Press":
            detector = ShoulderPressDetector()
            final_angles = {"elbow_l": 95.0, "elbow_r": 95.0, "extension": "Low", "symmetry": "Balanced"}
        else:
            return 0, {}
        st.session_state.video_detector = detector
        st.session_state.video_prev_reps = prev_reps

    # 2. Configure MediaPipe Pose Landmarker in VIDEO mode (Cached in session state to prevent reload freezing on rerun!)
    if "mp_detector" not in st.session_state or st.session_state.mp_detector is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.abspath(os.path.join(current_dir, "..", "..", "ml_models", "pose_landmarker_full.task"))
        try:
            base_options = python.BaseOptions(model_asset_path=model_path)
            options = vision.PoseLandmarkerOptions(
                base_options=base_options,
                running_mode=vision.RunningMode.VIDEO,
                output_segmentation_masks=False
            )
            st.session_state.mp_detector = vision.PoseLandmarker.create_from_options(options)
        except Exception as e:
            status_placeholder.error(f"Failed to load MediaPipe Pose model: {str(e)}")
            return 0, {}
            
    mp_detector = st.session_state.mp_detector

    # 3. Open Video File
    cap = cv2.VideoCapture(file_path)
    if not cap.isOpened():
        status_placeholder.error("Could not open uploaded video file.")
        return 0, {}

    # Retrieve video metadata
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or np.isnan(fps):
        fps = 30.0  # Fallback
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    start_frame = st.session_state.get("video_frame_index", 0)
    if start_frame > 0:
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        frame_index = start_frame
    else:
        frame_index = 0
    
    start_processing_time = time.time()
    
    # 4. Process frame-by-frame loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_index += 1
        h, w, _ = frame.shape
        
        # Downscale frame if too large to accelerate processing and fit the container width perfectly
        target_width = 640
        if w > target_width:
            aspect_ratio = target_width / w
            frame = cv2.resize(frame, (target_width, int(h * aspect_ratio)), interpolation=cv2.INTER_AREA)
            h, w, _ = frame.shape

        # Calculate exact timestamp in milliseconds for MediaPipe video tracking
        timestamp_ms = int((frame_index / fps) * 1000)
        
        # Convert frame color scheme BGR -> RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # Execute Pose Tracking
        try:
            result = mp_detector.detect_for_video(mp_image, timestamp_ms)
            
            if result.pose_landmarks and len(result.pose_landmarks) > 0:
                landmarks = result.pose_landmarks[0]
                
                # Update Joint Posture Detector
                biometrics = detector.process(landmarks)
                final_angles = biometrics
                
                # Draw overlays
                draw_skeleton(frame, landmarks)
                draw_hud(frame, detector.reps, detector.stage, detector.feedback, exercise_name, final_angles)
            else:
                draw_hud(frame, detector.reps, "Wait", "Positioning: step back so your full body is visible.", exercise_name)
        except Exception as e:
            # Safely log framework processing warning directly inside frame
            cv2.rectangle(frame, (10, h - 50), (w - 10, h - 10), (0, 0, 150), -1)
            cv2.putText(frame, f"Analysis Error: {str(e)[:50]}", (20, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Convert back to RGB for Streamlit rendering
        display_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_placeholder.image(display_frame_rgb, use_container_width=True)
        
        # Render real-time progress banner below the canvas showing AI Coach Guideline
        percentage = min(100, int((frame_index / total_frames) * 100)) if total_frames > 0 else 0
        status_placeholder.markdown(f"""
        <div style="background: rgba(0, 255, 204, 0.05); border: 1px solid rgba(0, 255, 204, 0.12); border-radius: 8px; padding: 12px; margin-top: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(0, 255, 204, 0.1); padding-bottom: 8px; margin-bottom: 8px;">
                <div style="font-size: 0.88rem; color: #00FFCC; font-weight: 700;">🤖 AI Biometrics Processing... {percentage}%</div>
                <div style="font-size: 0.88rem; color: #ffffff; font-weight: 600;">Counted: <span style="color: #00FFCC;">{detector.reps} reps</span></div>
            </div>
            <div style="font-size: 0.88rem; color: #cbd5e1; font-weight: 400; display: flex; align-items: center; gap: 6px;">
                <span style="font-size: 1rem;">🎙️</span>
                <span><b>Coach Feedback:</b> "{st.session_state.get('feedback_cue', '')}"</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Synchronize angles into session state instantly so sidebar biometrics gauges move dynamically
        st.session_state.simulated_angles[exercise_name.lower().replace(" ", "_").replace("-", "_")] = final_angles
        
        # Dynamically update the sidebar biometrics placeholder in real-time inside the frame-by-frame loop!
        if "metrics_placeholder" in st.session_state and st.session_state.metrics_placeholder is not None:
            try:
                with st.session_state.metrics_placeholder.container():
                    from services.ui.exercise_sidebar import render_exercise_metrics
                    render_exercise_metrics(exercise_name, final_angles)
            except Exception as e:
                pass
        
        # Always synchronize real-time posture feedback cue so that voice coach/UI reads it
        st.session_state.feedback_cue = detector.feedback

        # Initialize current rep warnings list if not already present
        if "current_rep_warnings" not in st.session_state:
            st.session_state.current_rep_warnings = []

        # Collect warnings observed during the current rep execution
        feedback_lower = detector.feedback.lower()
        is_warning = any(word in feedback_lower for word in ["warning", "check", "sag", "lean", "feet", "arm", "positioning", "wrist"])
        if is_warning:
            warning_text = detector.feedback
            if warning_text not in st.session_state.current_rep_warnings:
                st.session_state.current_rep_warnings.append(warning_text)

        # Check if a new rep is detected during video playback to sync reps & sets in real-time
        if detector.reps > prev_reps:
            # Capture the errors compiled during this completed rep
            rep_errors = list(st.session_state.current_rep_warnings)
            
            from services.state.session import trigger_rep_success
            trigger_rep_success()
            prev_reps = detector.reps
            st.session_state.video_prev_reps = prev_reps
            
            # Reset the rep warnings buffer for the next rep
            st.session_state.current_rep_warnings = []

            # Query the Groq voice coach asynchronously in a background thread to prevent blocking/freezing the video playback loop!
            import threading
            
            def run_coaching_voice_async(ex_name, curr_set, curr_reps, tgt_sets, tgt_reps, errors, angles, placeholder):
                try:
                    from services.coaching.groq_coach import trigger_coaching_audio
                    audio_b64 = trigger_coaching_audio(
                        exercise_name=ex_name,
                        current_set=curr_set,
                        current_reps=curr_reps,
                        target_sets=tgt_sets,
                        target_reps=tgt_reps,
                        rep_errors=errors,
                        angles_dict=angles
                    )
                    if audio_b64:
                        import base64
                        audio_bytes = base64.b64decode(audio_b64)
                        # Play voice feedback instantly using native Streamlit audio player with autoplay
                        placeholder.audio(audio_bytes, format="audio/mp3", autoplay=True)
                except Exception as e:
                    print(f"Async voice coaching failed: {str(e)}")
                    
            threading.Thread(
                target=run_coaching_voice_async,
                args=(exercise_name, st.session_state.current_set, st.session_state.current_reps, st.session_state.target_sets, st.session_state.target_reps, rep_errors, final_angles, audio_placeholder),
                daemon=True
            ).start()

        # Keep track of the current frame index for seamless resuming across reruns
        st.session_state.video_frame_index = frame_index
        
        # Control playback timing to match the video's original FPS (pacing)
        elapsed_processing = time.time() - start_processing_time
        target_elapsed = frame_index / fps
        sleep_duration = target_elapsed - elapsed_processing
        if sleep_duration > 0:
            time.sleep(sleep_duration)

    cap.release()
    return detector.reps, final_angles


def draw_skeleton(img, landmarks):
    """
    Draws custom pose skeleton connecting lines and neon joint dots.
    """
    h, w, _ = img.shape
    connections = [
        (11, 12), (11, 23), (12, 24), (23, 24), # Core Torso
        (11, 13), (13, 15), (12, 14), (14, 16), # Arms
        (23, 25), (25, 27), (24, 26), (26, 28)  # Legs
    ]
    
    points = {}
    for idx in range(33):
        lm = landmarks[idx]
        if lm.visibility > 0.45:
            cx, cy = int(lm.x * w), int(lm.y * h)
            points[idx] = (cx, cy)
            
            # Neon cyan dots
            cv2.circle(img, (cx, cy), 5, (204, 255, 0), -1)
            cv2.circle(img, (cx, cy), 7, (204, 255, 0), 1)
            
    for p1, p2 in connections:
        if p1 in points and p2 in points:
            # Electric blue lines
            cv2.line(img, points[p1], points[p2], (255, 153, 0), 2, cv2.LINE_AA)


def draw_hud(img, reps, stage, feedback, exercise_name, angles=None):
    """
    Draws translucent premium HUD and statistics directly on frames.
    """
    h, w, _ = img.shape
    overlay = img.copy()
    
    # Header translucent bar
    cv2.rectangle(overlay, (0, 0), (w, 75), (15, 8, 3), -1)
    # Footer translucent bar
    cv2.rectangle(overlay, (0, h - 60), (w, h), (15, 8, 3), -1)
    
    # Overlay blending
    alpha = 0.62
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    
    # Texts
    cv2.putText(img, "🏋️ FIT-AI VIDEO ANALYSIS", (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.62, (204, 255, 0), 2, cv2.LINE_AA)
    cv2.putText(img, f"EXERCISE: {exercise_name.upper()}", (15, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 200, 200), 1, cv2.LINE_AA)
    
    # Stats
    cv2.putText(img, f"REPS: {reps}", (w - 180, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (204, 255, 0), 3, cv2.LINE_AA)
    cv2.putText(img, f"STAGE: {stage.upper()}", (w - 330, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    
    # Draw real-time joint angles in the footer bar above the feedback
    if angles:
        angles_str = "  ".join(f"{k.upper().replace('_', ' ')}: {float(v):.1f}°" for k, v in angles.items() if isinstance(v, (int, float)))
        cv2.putText(img, angles_str, (15, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (204, 255, 0), 1, cv2.LINE_AA)

    # Feedback color coding
    text_color = (255, 255, 255)
    if "Warning" in feedback or "Form" in feedback or "Align" in feedback:
        text_color = (51, 51, 255) # Warning Red
    elif "Excellent" in feedback or "Good" in feedback or "Perfect" in feedback or "Solid" in feedback:
        text_color = (204, 255, 0) # Success Cyan
        
    cv2.putText(img, feedback, (15, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.52, text_color, 1, cv2.LINE_AA)
