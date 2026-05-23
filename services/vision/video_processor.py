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

def process_uploaded_video(file_path, exercise_name, image_placeholder, status_placeholder):
    """
    Parses a recorded workout video frame-by-frame, runs posture biometrics
    using MediaPipe Pose Landmarker (VIDEO mode), overlays pose skeletons/HUDs,
    and streams them to the Streamlit canvas at native frame rates.
    
    Returns:
        total_reps (int): total repetitions completed
        final_angles (dict): final joint angles/biometrics state
    """
    # 1. Initialize selected exercise detector
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

    # 2. Configure MediaPipe Pose Landmarker in VIDEO mode
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.abspath(os.path.join(current_dir, "..", "..", "ml_models", "pose_landmarker_full.task"))
    
    try:
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            output_segmentation_masks=False
        )
        mp_detector = vision.PoseLandmarker.create_from_options(options)
    except Exception as e:
        status_placeholder.error(f"Failed to load MediaPipe Pose model: {str(e)}")
        return 0, {}

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
    
    frame_index = 0
    start_processing_time = time.time()
    
    # 4. Process frame-by-frame loop
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_index += 1
        h, w, c = frame.shape
        
        # Downscale frame if too large to accelerate processing and fit the container width perfectly
        target_width = 640
        if w > target_width:
            aspect_ratio = target_width / w
            frame = cv2.resize(frame, (target_width, int(h * aspect_ratio)), interpolation=cv2.INTER_AREA)
            h, w, c = frame.shape

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
                draw_hud(frame, detector.reps, detector.stage, detector.feedback, exercise_name)
            else:
                draw_hud(frame, detector.reps, "Wait", "Positioning: step back so your full body is visible.", exercise_name)
        except Exception as e:
            # Safely log framework processing warning directly inside frame
            cv2.rectangle(frame, (10, h - 50), (w - 10, h - 10), (0, 0, 150), -1)
            cv2.putText(frame, f"Analysis Error: {str(e)[:50]}", (20, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1)

        # Convert back to RGB for Streamlit rendering
        display_frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_placeholder.image(display_frame_rgb, use_container_width=True)
        
        # Render real-time progress banner below the canvas
        percentage = min(100, int((frame_index / total_frames) * 100)) if total_frames > 0 else 0
        status_placeholder.markdown(f"""
        <div style="background: rgba(0, 255, 204, 0.05); border: 1px solid rgba(0, 255, 204, 0.12); border-radius: 8px; padding: 10px; display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 0.88rem; color: #00FFCC; font-weight: 700;">🤖 AI Biometrics Processing... {percentage}%</div>
            <div style="font-size: 0.88rem; color: #ffffff; font-weight: 600;">Counted: <span style="color: #00FFCC;">{detector.reps} reps</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Synchronize angles into session state instantly so sidebar biometrics gauges move dynamically
        st.session_state.simulated_angles[exercise_name.lower().replace(" ", "_").replace("-", "_")] = final_angles
        st.session_state.feedback_cue = detector.feedback
        
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
    h, w, c = img.shape
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


def draw_hud(img, reps, stage, feedback, exercise_name):
    """
    Draws translucent premium HUD and statistics directly on frames.
    """
    h, w, c = img.shape
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
    
    # Feedback color coding
    text_color = (255, 255, 255)
    if "Warning" in feedback or "Form" in feedback or "Align" in feedback:
        text_color = (51, 51, 255) # Warning Red
    elif "Excellent" in feedback or "Good" in feedback or "Perfect" in feedback or "Solid" in feedback:
        text_color = (204, 255, 0) # Success Cyan
        
    cv2.putText(img, feedback, (15, h - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.55, text_color, 1, cv2.LINE_AA)
