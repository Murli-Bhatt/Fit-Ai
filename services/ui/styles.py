import streamlit as st

def apply_global_styles():
    """
    Applies the unified, premium dark-mode styling and glassmorphic UI elements
    across the entire FIT-AI Gym Trainer application.
    """
    st.markdown("""
    <style>
        /* Import Premium Typography */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Global App Background Styling */
        .stApp {
            background: radial-gradient(circle at top center, #0f172a 0%, #020617 100%) !important;
            color: #f8fafc !important;
        }
        
        /* Glassmorphism Floating Login Card */
        .login-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.6) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 24px;
            padding: 45px 35px;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(16px);
            margin: auto;
            max-width: 450px;
            text-align: center;
        }
        
        .brand-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00FFCC 0%, #0099FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            letter-spacing: 2px;
        }
        
        .brand-subtitle {
            font-size: 0.95rem;
            color: #94a3b8;
            font-weight: 300;
            margin-bottom: 30px;
            letter-spacing: 0.5px;
        }
        
        /* Sidebar Custom Styles */
        section[data-testid="stSidebar"] {
            background-color: #030712 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.03) !important;
            box-shadow: inset -10px 0 30px rgba(0, 0, 0, 0.5) !important;
        }
        
        /* Glowing Form Section Headers */
        .form-heading {
            color: #ffffff;
            font-size: 1.35rem;
            font-weight: 600;
            margin-bottom: 24px;
            text-align: left;
            border-left: 4px solid #00FFCC;
            padding-left: 12px;
            letter-spacing: 0.5px;
        }
        
        /* Main Welcome Hero Banner */
        .hero-container {
            background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(0, 255, 204, 0.08);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #00FFCC 0%, #0099FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        
        .hero-subtitle {
            font-size: 1.15rem;
            color: #94a3b8;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        /* Glassmorphic Grid Cards */
        .card {
            background: rgba(255, 255, 255, 0.01);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }
        
        .card:hover {
            transform: translateY(-4px);
            background: rgba(255, 255, 255, 0.03);
            border-color: rgba(0, 255, 204, 0.25);
            box-shadow: 0 12px 30px rgba(0, 255, 204, 0.08);
        }
        
        .card-icon {
            font-size: 2.2rem;
            margin-bottom: 12px;
            display: inline-block;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #00FFCC;
            margin-bottom: 8px;
        }
        
        .card-desc {
            font-size: 0.9rem;
            color: #94a3b8;
            line-height: 1.5;
            font-weight: 300;
        }
        
        /* Custom Styling for Tabs */
        div.stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            justify-content: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
            padding-bottom: 4px;
        }
        
        div.stTabs [data-baseweb="tab"] {
            background-color: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 20px !important;
            padding: 8px 24px !important;
            color: #64748b !important;
            font-weight: 600 !important;
            transition: all 0.25s ease !important;
        }
        
        div.stTabs [data-baseweb="tab"]:hover {
            color: #ffffff !important;
            background-color: rgba(255, 255, 255, 0.02) !important;
        }
        
        div.stTabs [aria-selected="true"] {
            background-color: rgba(0, 255, 204, 0.06) !important;
            border-color: rgba(0, 255, 204, 0.3) !important;
            color: #00FFCC !important;
            box-shadow: 0 0 12px rgba(0, 255, 204, 0.05) !important;
        }
        
        /* Crisp Widget Labels */
        div[data-testid="stWidgetLabel"] p {
            color: #cbd5e1 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
        }
        
        /* Custom Premium Inputs Styling - Extremely robust to enforce dark backgrounds and prevent white-on-white text */
        div[data-baseweb="input"] {
            background-color: #0c0f19 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            transition: all 0.25s ease !important;
        }
        
        div[data-baseweb="input"]:focus-within {
            border-color: rgba(0, 255, 204, 0.5) !important;
            box-shadow: 0 0 12px rgba(0, 255, 204, 0.15) !important;
            background-color: #0c0f19 !important;
        }
        
        /* Force actual input field inside BaseWeb wrappers to be dark and text white */
        div[data-baseweb="input"] input {
            background-color: transparent !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            border: none !important;
        }
        
        div[data-testid="stTextInput"] input, 
        div[data-testid="stNumberInput"] input {
            background-color: transparent !important;
            color: #ffffff !important;
            caret-color: #00FFCC !important;
        }
        
        /* Override browser autocomplete/autofill styles to keep them dark */
        input:-webkit-autofill,
        input:-webkit-autofill:hover, 
        input:-webkit-autofill:focus, 
        input:-webkit-autofill:active {
            -webkit-text-fill-color: #ffffff !important;
            -webkit-box-shadow: 0 0 0px 1000px #0c0f19 inset !important;
            transition: background-color 5000s ease-in-out 0s !important;
        }
        
        /* Input placeholder color */
        div[data-baseweb="input"] input::placeholder {
            color: #64748b !important;
            opacity: 0.7 !important;
        }
        
        /* Selectbox Container Styling - Dark themed and glowing borders */
        div[data-testid="stSelectbox"] > div [role="combobox"] {
            background-color: #0c0f19 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            transition: all 0.25s ease !important;
            padding: 4px 12px !important;
        }
        
        div[data-testid="stSelectbox"] > div [role="combobox"]:hover {
            border-color: rgba(0, 255, 204, 0.3) !important;
            background-color: #0c0f19 !important;
        }
        
        /* Expander Premium Styling */
        div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.01) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            overflow: hidden !important;
        }
        
        div[data-testid="stExpander"] > details > summary {
            background-color: transparent !important;
            color: #ffffff !important;
            font-weight: 600 !important;
            padding: 12px 16px !important;
            transition: all 0.25s ease !important;
        }
        
        div[data-testid="stExpander"] > details > summary:hover {
            color: #00FFCC !important;
            background-color: rgba(0, 255, 204, 0.02) !important;
        }
        
        div[data-testid="stExpander"] [data-testid="stExpanderDetails"] {
            padding: 16px !important;
            background-color: rgba(0, 0, 0, 0.15) !important;
            border-top: 1px solid rgba(255, 255, 255, 0.03) !important;
        }
        
        /* Glassmorphic Metrics Card */
        .stat-card {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.02) 0%, rgba(255, 255, 255, 0.005) 100%);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .stat-card:hover {
            border-color: rgba(0, 255, 204, 0.2);
            background: rgba(255, 255, 255, 0.03);
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(0, 0, 0, 0.3);
        }
        
        /* Coach Voice Cue Speech Box */
        .speech-box {
            background: linear-gradient(135deg, rgba(0, 255, 204, 0.02) 0%, rgba(0, 153, 255, 0.02) 100%);
            border: 1px solid rgba(0, 255, 204, 0.15);
            border-radius: 14px;
            padding: 14px;
            box-shadow: inset 0 0 12px rgba(0, 255, 204, 0.02);
            position: relative;
        }
        
        /* Progress Table Styling */
        .row-active {
            background: rgba(0, 255, 204, 0.02);
            border-left: 3px solid #00FFCC;
        }
        .row-completed {
            opacity: 0.8;
            background: rgba(0, 230, 118, 0.01);
        }
        .row-pending {
            opacity: 0.6;
        }
        
        /* Status Badges */
        .status-badge {
            border-radius: 20px;
            padding: 4px 10px;
            font-size: 0.72rem;
            font-weight: 700;
            letter-spacing: 0.5px;
            display: inline-block;
            text-align: center;
        }
        
        .badge-completed {
            background: rgba(0, 230, 118, 0.1);
            border: 1px solid rgba(0, 230, 118, 0.25);
            color: #00FF99;
        }
        
        .badge-active {
            background: rgba(0, 255, 204, 0.1);
            border: 1px solid rgba(0, 255, 204, 0.35);
            color: #00FFCC;
            box-shadow: 0 0 10px rgba(0, 255, 204, 0.1);
            animation: pulse-active-glow 2s infinite ease-in-out;
        }
        
        .badge-pending {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            color: #8b949e;
        }
        
        @keyframes pulse-active-glow {
            0% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0.3); }
            70% { box-shadow: 0 0 0 5px rgba(0, 255, 204, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 255, 204, 0); }
        }
        
        /* Footer Styling */
        .footer {
            text-align: center;
            padding: 25px 0;
            color: #475569;
            font-size: 0.8rem;
            border-top: 1px solid rgba(255, 255, 255, 0.03);
            margin-top: 50px;
            letter-spacing: 0.5px;
        }
        
        /* Hide Streamlit Defaults */
        #MainMenu {visibility: hidden; display: none !important;}
        footer {visibility: hidden; display: none !important;}
        header {visibility: hidden; display: none !important;}
        div[data-testid="stHeader"] {visibility: hidden; display: none !important;}
        div[data-testid="stDecoration"] {display: none !important;}
        
        /* Dynamic Button Custom Styling to prevent white-on-white text */
        div.stButton > button {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border-radius: 14px !important;
            font-size: 0.95rem !important;
            padding: 10px 24px !important;
            font-weight: 600 !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            letter-spacing: 0.5px !important;
        }
        
        /* Secondary Buttons (e.g. Sign Out, Stop) */
        div.stButton > button[data-testid="baseButton-secondary"] {
            background-color: rgba(255, 255, 255, 0.02) !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        div.stButton > button[data-testid="baseButton-secondary"]:hover {
            border-color: #00FFCC !important;
            color: #00FFCC !important;
            background-color: rgba(0, 255, 204, 0.04) !important;
            box-shadow: 0 4px 15px rgba(0, 255, 204, 0.1) !important;
            transform: translateY(-2px) !important;
        }
        
        /* Primary Action Buttons (e.g. Login, Start Workout) */
        div.stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #00FFCC 0%, #0099FF 100%) !important;
            color: #020617 !important;
            font-weight: 700 !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0, 255, 204, 0.15) !important;
        }
        
        div.stButton > button[data-testid="baseButton-primary"]:hover {
            box-shadow: 0 6px 20px rgba(0, 255, 204, 0.3) !important;
            transform: translateY(-2px) !important;
            color: #020617 !important;
        }
        
        div.stButton > button:active {
            transform: translateY(0px) !important;
        }
        
        /* Modern Dataframe/Table customization */
        div[data-testid="stDataFrame"] {
            background: rgba(255, 255, 255, 0.01) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            padding: 8px !important;
        }
    </style>
    """, unsafe_allow_html=True)
