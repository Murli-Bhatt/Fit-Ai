import streamlit as st

def apply_global_styles():
    """
    Applies the unified, premium dark-mode styling and glassmorphic UI elements
    across the entire FIT-AI Gym Trainer application.
    """
    st.markdown("""
    <style>
        /* Import Premium Typography */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
        
        * {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Global App Background Styling */
        .stApp {
            background: radial-gradient(circle at top right, #111827 0%, #030712 100%) !important;
            color: #f3f4f6 !important;
        }
        
        /* Glassmorphism Floating Login Card */
        .login-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 24px;
            padding: 40px 30px;
            box-shadow: 0 20px 45px rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(12px);
            margin: auto;
            max-width: 450px;
            text-align: center;
        }
        
        .brand-title {
            font-size: 2.6rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00FFCC 0%, #0099FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
            letter-spacing: 1.5px;
        }
        
        .brand-subtitle {
            font-size: 0.95rem;
            color: #9ca3af;
            font-weight: 300;
            margin-bottom: 30px;
        }
        
        /* Sidebar custom styles */
        section[data-testid="stSidebar"] {
            background-color: #0c0f17 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Glowing Form Section Headers */
        .form-heading {
            color: #ffffff;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 20px;
            text-align: left;
            border-left: 4px solid #00FFCC;
            padding-left: 12px;
        }
        
        /* Main Welcome Hero Banner */
        .hero-container {
            background: linear-gradient(90deg, #1b2330 0%, #0f141c 100%);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
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
            color: #9ca3af;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        /* Glassmorphic Grid Cards */
        .card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }
        
        .card:hover {
            transform: translateY(-4px);
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(0, 255, 204, 0.3);
            box-shadow: 0 12px 30px rgba(0, 255, 204, 0.1);
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
            color: #cbd5e1;
            line-height: 1.5;
            font-weight: 300;
        }
        
        /* Custom Styling for Tabs */
        div.stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            justify-content: center;
        }
        
        div.stTabs [data-baseweb="tab"] {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 20px !important;
            padding: 8px 24px !important;
            color: #9ca3af !important;
            font-weight: 600 !important;
        }
        
        div.stTabs [aria-selected="true"] {
            background-color: rgba(0, 255, 204, 0.1) !important;
            border-color: rgba(0, 255, 204, 0.4) !important;
            color: #00FFCC !important;
        }
        
        /* Footer Styling */
        .footer {
            text-align: center;
            padding: 25px 0;
            color: #6b7280;
            font-size: 0.8rem;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            margin-top: 50px;
        }
    </style>
    """, unsafe_allow_html=True)
