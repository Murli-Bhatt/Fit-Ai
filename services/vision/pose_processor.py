import cv2
import av
import os
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

class PoseVideoProcessor:
    """
    Background WebRTC Video Processor that processes frames, executes posture
    biometrics tracking using MediaPipe Pose Landmarker, and draws a glowing skeleton & HUD overlay.
    """
    def __init__(self, exercise_name):
        self.exercise_name = exercise_name
        self.reps = 0
        self.feedback = "Positioning camera... align your full body."
        self.angles = {}
        self.new_rep_detected = False
        self.new_feedback_detected = False
        self.last_spoken_time = 0.0
        self.last_spoken_feedback = ""
        self.current_rep_warnings = []
        
        # Initialize selected exercise detector
        if exercise_name == "Squats":
            self.detector = SquatDetector()
            self.angles = {"knee": 170.0, "hip": 170.0, "depth": "Standing", "back": "Neutral Spine"}
        elif exercise_name == "Push-ups":
            self.detector = PushupDetector()
            self.angles = {"elbow": 175.0, "torso": 178.0, "depth": "Top Plank", "symmetry": "Balanced"}
        elif exercise_name == "Bicep Curls":
            self.detector = BicepCurlDetector()
            self.angles = {"elbow_l": 165.0, "elbow_r": 165.0, "stability": "High", "range": "Full Extension"}
        elif exercise_name == "Plank":
            self.detector = PlankDetector()
            self.angles = {"hip": 178.0, "elbow": 90.0, "stability": "Optimal", "duration": 0}
        elif exercise_name == "Lunges":
            self.detector = LungeDetector()
            self.angles = {"front_knee": 170.0, "back_knee": 165.0, "torso": "Straight", "depth": "Standing"}
        elif exercise_name == "Shoulder Press":
            self.detector = ShoulderPressDetector()
            self.angles = {"elbow_l": 95.0, "elbow_r": 95.0, "extension": "Low", "symmetry": "Balanced"}
            
        # Absolute path resolution for the MediaPipe model file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.abspath(os.path.join(current_dir, "..", "..", "ml_models", "pose_landmarker_full.task"))
        self.mp_initialized = False
        self.mp_detector = None
        self.model_error_occurred = False
            
    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        """
        Receives an input video frame, performs posture assessment,
        overlays biometrics & HUD details, and returns the modified frame.
        """
        img = frame.to_ndarray(format="bgr24")
        
        # Mirror the frame horizontally so that the user's left/right matches real-world anatomy
        # This resolves the live webcam left/right mismatch issue perfectly!
        img = cv2.flip(img, 1)
        
        h, w, _ = img.shape
        
        # Verify model loaded successfully or initialize on first frame in the background WebRTC thread
        if not self.mp_initialized and not self.model_error_occurred:
            try:
                base_options = python.BaseOptions(model_asset_path=self.model_path)
                options = vision.PoseLandmarkerOptions(
                    base_options=base_options,
                    running_mode=vision.RunningMode.IMAGE,
                    output_segmentation_masks=False
                )
                self.mp_detector = vision.PoseLandmarker.create_from_options(options)
                self.mp_initialized = True
            except Exception as e:
                self.model_error_occurred = True
                self.feedback = f"Error loading pose_landmarker_full.task: {str(e)}"
                
        if self.model_error_occurred or not self.mp_initialized:
            # Draw eye-catching red warning box
            cv2.rectangle(img, (10, 10), (w - 10, 90), (0, 0, 200), -1)
            cv2.putText(img, "FIT-AI VISION ERROR", (20, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
            cv2.putText(img, self.feedback[:60], (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            return av.VideoFrame.from_ndarray(img, format="bgr24")
            
        # Convert OpenCV BGR representation to RGB for MediaPipe Tasks
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_image)
        
        try:
            result = self.mp_detector.detect(mp_image)
            
            if result.pose_landmarks and len(result.pose_landmarks) > 0:
                landmarks = result.pose_landmarks[0]
                
                # 1. Run the posture logic detector
                biometrics = self.detector.process(landmarks)
                
                # 2. Update thread-accessible variables
                self.angles = biometrics
                self.feedback = self.detector.feedback
                
                if self.detector.reps > self.reps:
                    self.reps = self.detector.reps
                    self.new_rep_detected = True
                    
                # Collect warnings observed during the current rep execution
                feedback_lower = self.detector.feedback.lower()
                is_warning = any(word in feedback_lower for word in ["warning", "check", "sag", "lean", "feet", "arm", "positioning", "wrist"])
                if is_warning:
                    warning_text = self.detector.feedback
                    if warning_text not in self.current_rep_warnings:
                        self.current_rep_warnings.append(warning_text)
                    
                # 3. Draw custom neon pose skeleton connection lines
                self.draw_skeleton(img, landmarks)
                
                # 4. Draw high-fidelity HUD card overlays
                self.draw_hud(img, self.reps, self.detector.stage, self.detector.feedback, self.angles)
            else:
                self.feedback = "Positioning check: step back so your full body is visible."
                self.draw_hud(img, self.reps, "Wait", self.feedback)
                
        except Exception as e:
            # Prevent crashes in the WebRTC loop by printing trace inside frame
            cv2.rectangle(img, (10, h - 70), (w - 10, h - 10), (0, 0, 180), -1)
            cv2.putText(img, f"Frame Process Crash: {str(e)[:50]}", (20, h - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")
        
    def draw_skeleton(self, img, landmarks):
        """
        Draws glowing connection lines and high-contrast joints.
        """
        h, w, _ = img.shape
        connections = [
            # Torso / Core alignment
            (11, 12), (11, 23), (12, 24), (23, 24),
            # Arms / Flexion
            (11, 13), (13, 15), (12, 14), (14, 16),
            # Legs / Flexion
            (23, 25), (25, 27), (24, 26), (26, 28)
        ]
        
        points = {}
        for idx in range(33):
            lm = landmarks[idx]
            # Draw only landmarks above minimum visibility threshold
            if lm.visibility > 0.45:
                cx, cy = int(lm.x * w), int(lm.y * h)
                points[idx] = (cx, cy)
                
                # Draw neon cyan joints
                cv2.circle(img, (cx, cy), 5, (204, 255, 0), -1) # BGR Neon Cyan/Green
                cv2.circle(img, (cx, cy), 7, (204, 255, 0), 1)
                
        for p1, p2 in connections:
            if p1 in points and p2 in points:
                # Draw electric blue connection lines
                cv2.line(img, points[p1], points[p2], (255, 153, 0), 2, cv2.LINE_AA) # BGR Electric Blue
                
    def draw_hud(self, img, reps, stage, feedback, angles=None):
        """
        Draws a modern, premium translucent HUD overlay directly on the frame.
        """
        h, w, _ = img.shape
        
        # 1. Compile glassmorphic overlay shapes
        overlay = img.copy()
        
        # Top Header Banner
        cv2.rectangle(overlay, (0, 0), (w, 75), (15, 8, 3), -1)
        # Bottom Footer Banner
        cv2.rectangle(overlay, (0, h - 60), (w, h), (15, 8, 3), -1)
        
        # Blend overlay (opacity 0.62)
        alpha = 0.62
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
        
        # 2. Draw HUD texts
        # Neon green color BGR: (204, 255, 0)
        # Warning Orange color BGR: (0, 165, 255)
        # Red warning color BGR: (102, 51, 255)
        cv2.putText(img, "🏋️ FIT-AI CAMERA", (15, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (204, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, f"EXERCISE: {self.exercise_name.upper()}", (15, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 200, 200), 1, cv2.LINE_AA)
        
        # Rep counter in the top right
        cv2.putText(img, f"REPS: {reps}", (w - 180, 48), cv2.FONT_HERSHEY_SIMPLEX, 0.95, (204, 255, 0), 3, cv2.LINE_AA)
        
        # Stage indicator
        cv2.putText(img, f"STAGE: {stage.upper()}", (w - 330, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
        
        # Draw real-time joint angles in the footer bar above the feedback
        if angles:
            angles_str = "  ".join(f"{k.upper().replace('_', ' ')}: {float(v):.1f}°" for k, v in angles.items() if isinstance(v, (int, float)))
            cv2.putText(img, angles_str, (15, h - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (204, 255, 0), 1, cv2.LINE_AA)

        # 3. Handle color coding for coaching feedback
        text_color = (255, 255, 255) # White default
        if "Warning" in feedback or "Form" in feedback or "Align" in feedback or "Cheating" in feedback:
            text_color = (51, 51, 255) # High-contrast Red for warnings
        elif "Excellent" in feedback or "Good" in feedback or "Perfect" in feedback or "Splendid" in feedback:
            text_color = (204, 255, 0) # Neon green for success
            
        cv2.putText(img, feedback, (15, h - 18), cv2.FONT_HERSHEY_SIMPLEX, 0.52, text_color, 1, cv2.LINE_AA)
