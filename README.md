# 🏋️ FIT-AI Gym Trainer: Real-Time AI Posture & Biometrics Coach

FIT-AI is an elite, highly interactive, and visually stunning web application that acts as your personal AI Gym Trainer. Combining advanced Computer Vision (MediaPipe Pose Estimation), real-time SQLite persistence, LLM-powered feedback (Groq Cloud API), and browser-synthesized voice coaching (gTTS), FIT-AI tracks your gym exercises, counts your reps, analyzes your posture, and gives you live verbal feedback!

---

## 🌟 Key Features

*   **🎥 Real-Time Webcam arena**: Stream live webcam video directly in your web browser via `streamlit-webrtc` with low latency.
*   **📤 Workout Video Uploader**: Upload pre-recorded workout videos (`.mp4`, `.mov`, `.avi`) and let the AI process your movement frame-by-frame.
*   **📐 Advanced Biomechanics Engine**: Employs real-time MediaPipe joint angle calculations to identify precise physical postures.
*   **🏋️ 6 Supported Core Exercises**:
    *   **Squats**: Depth tracking, back-angle warnings, knee cave/alignment checks.
    *   **Lunges**: Knee flexion depth, back straightness, balance analytics.
    *   **Planks**: Spine alignment (hip sag / hip rise detection).
    *   **Push-ups**: Flexion depth, spine straightness, chest-to-ground checks.
    *   **Bicep Curls**: Full range of motion, elbow flare/displacement warnings.
    *   **Shoulder Presses**: Range of motion, overhead lockouts, elbow angles.
*   **🧠 Groq-Powered AI Coaching**: Connects to the ultra-fast Llama-3.1 model to generate highly actionable, motivational, and contextual personal training guidance upon completing a repetition.
*   **🎙️ Live Voice Feedback**: TTS synthesizes voice guidance and plays it instantly inside your browser as if a trainer is standing right beside you.
*   **🔐 Local Authentication**: Secure login, password hashing, and user registration system.
*   **📊 SQLite Analytical Dashboard**: Tracks lifetime reps, session completion, and detailed daily logs with Pandas analytics.

---

## 🛠️ Technology Stack

*   **Frontend & Web UI**: Streamlit (with bespoke premium glassmorphic dark-theme custom CSS)
*   **WebRTC Streaming**: `streamlit-webrtc` & PyAV
*   **Computer Vision**: Google MediaPipe (Pose Landmark Model) & OpenCV
*   **AI Coach (LLM)**: Groq API (`llama-3.1-8b-instant`)
*   **Speech Generation**: gTTS (Google Text-To-Speech)
*   **Database Persistent Layer**: SQLite3
*   **Data Analysis**: Pandas & Numpy

---

## 📁 Project Architecture

```text
AI_GYM_Trainer/
│
├── app.py                      # Main entrypoint, application routing & Streamlit dashboard
├── requirements.txt            # Python environment dependencies
├── .gitignore                  # Git patterns to exclude (ignores local DB, credentials, and venvs)
├── .env.example                # Template configuration file for environmental API keys
│
├── core/                       # Biomechanical calculators
│   └── math_utils.py           # Core geometry (3D vectors, joint angle calculations)
│
├── detectors/                  # Specialized posture & repetition processors
│   ├── base_detector.py        # Abstract Base Class for exercise tracking
│   ├── squat_detector.py       # Squat tracking & depth validation
│   ├── bicep_curl_detector.py  # Bicep curl tracking & range validation
│   ├── lunge_detector.py       # Lunge range & balance tracking
│   ├── plank_detector.py       # Spine/hip alignment plank tracker
│   ├── pushup_detector.py      # Push-up depth & hip alignment tracker
│   └── shoulder_press_detector.py # Shoulder press extension tracker
│
├── services/                   # Business logic layers & helper packages
│   ├── auth/                   # Secure login & user registration handlers
│   ├── coaching/               # Groq LLM API client & voice text-to-speech converters
│   ├── persistence/            # SQLite3 database migrations & repository logs
│   ├── state/                  # Streamlit global session state handlers
│   ├── ui/                     # CSS template files, navigation, and sidebar widgets
│   └── vision/                 # WebRTC camera thread frames & video file parser
│
└── data/                       # Ignored folder where the local SQLite file (data.db) is stored
```

---

## ⚙️ Local Installation & Setup

Get FIT-AI up and running locally on your computer in just 5 steps:

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd AI_GYM_Trainer
```

### 2. Create and Activate a Virtual Environment
*   **Windows**:
    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    ```
*   **macOS / Linux**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

### 3. Install Required Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure Environmental Secrets
Create a `.env` file at the root of the project to insert your credentials. A template is provided in `.env.example`:
```bash
# Duplicate the example file
cp .env.example .env
```
Open `.env` and fill in your Groq API Key:
```env
groq_api_key = "YOUR_GROQ_API_KEY_HERE"
```
> 💡 *Note: You can sign up for a free, ultra-fast API key at [Groq Console](https://console.groq.com/).*

### 5. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
The application will automatically open in a new tab at `http://localhost:8501`.

---

## 🚀 Deployment Guide

FIT-AI is ready for instant cloud deployment. The easiest and most recommended path is deploying to **Streamlit Community Cloud**, which natively supports webcam feeds and audio player streams.

### Streamlit Community Cloud Deployment
1.  **Push Your Code to GitHub**:
    Ensure all files (excluding secrets and databases ignored in `.gitignore`) are pushed to a public or private GitHub repository.
2.  **Deploy on Streamlit**:
    *   Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
    *   Click **New app**, select your repository, branch (`main`), and set the main file path to `app.py`.
3.  **Configure API Secrets**:
    *   Before clicking deploy, click on the **Advanced Settings** dropdown.
    *   In the **Secrets** text area, paste your Groq API key:
        ```toml
        groq_api_key = "gsk_your_actual_groq_api_key_here"
        ```
    *   Click **Save** and click **Deploy**.
4.  **Open the Web App**:
    Your application will spin up in minutes! Streamlit Community Cloud will host your web app with an active SSL certificate (HTTPS), which is **required** by web browsers to grant permission for webcam access.

---

## 🔒 Security & Best Practices

*   **API Key Protection**: The project is pre-configured with `.gitignore` to prevent committing your `.env` or local databases (`data/`) to GitHub. Never commit active keys!
*   **Browser Permissions**: The live camera stream relies on `getUserMedia` API. Browsers require a secure context (**HTTPS** or **localhost**) to use the camera. When deploying, ensure your hosting domain has an active SSL certificate (HTTPS).
*   **Database Persistence**: When deploying on ephemeral cloud environments (like Streamlit Cloud or Hugging Face Spaces), the local SQLite database resets whenever the container restarts or goes to sleep. For robust multi-user persistence, connect to a hosted PostgreSQL/MySQL database by modifying `services/persistence/database.py`.

---

## 🤝 Contributing & Support

If you have questions, run into issues, or want to contribute new exercise detectors:
1.  Fork the project repository.
2.  Create your feature branch (`git checkout -b feature/AmazingDetector`).
3.  Commit your changes (`git commit -m 'Add Squat Jump Detector'`).
4.  Push the branch (`git push origin feature/AmazingDetector`).
5.  Open a Pull Request.

Happy training! 🏋️‍♂️ Let's make every single rep count!
