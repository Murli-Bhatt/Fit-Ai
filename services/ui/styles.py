import streamlit as st

def apply_global_styles():
    """
    Applies the unified, premium dark-mode styling across the FIT-AI Gym Trainer.
    Centres the login interface when logged out, and enables a fixed, scrollable
    sidebar with custom scrollbars when logged in.
    """
    is_logged_in = st.session_state.get("logged_in", False)
    
    # 1. Conditional Layout: Center login page or shift for fixed sidebar
    if is_logged_in:
        layout_css = """
        /* Force sidebar to be expanded and visible at all times */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            transform: none !important;
            margin-left: 0 !important;
            width: 320px !important;
            min-width: 320px !important;
            max-width: 320px !important;
            visibility: visible !important;
            display: flex !important;
            flex-direction: column !important;
            z-index: 999999 !important;
            background: linear-gradient(180deg, #060d1f 0%, #030712 100%) !important;
            border-right: 1px solid rgba(0, 255, 204, 0.07) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.6) !important;
            overflow-y: auto !important;
            height: 100vh !important;
        }

        /* Adjust main app container to respect the fixed sidebar */
        div[data-testid="stAppViewContainer"] {
            margin-left: 320px !important;
            width: calc(100% - 320px) !important;
        }

        /* Enable vertical scrolling inside inner sidebar container */
        section[data-testid="stSidebar"] > div:first-child,
        div[data-testid="stSidebarUserContent"] {
            overflow-y: auto !important;
            height: 100% !important;
        }

        /* Completely hide scrollbars inside the sidebar to prevent visual clutter */
        section[data-testid="stSidebar"]::-webkit-scrollbar,
        section[data-testid="stSidebar"] *::-webkit-scrollbar {
            display: none !important;
            width: 0px !important;
            height: 0px !important;
            background: transparent !important;
        }
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"] * {
            -ms-overflow-style: none !important;
            scrollbar-width: none !important;
        }
        """
    else:
        layout_css = """
        /* Completely hide sidebar on login screen to allow centering */
        section[data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
            width: 0px !important;
        }

        /* Center the login/registration interface */
        div[data-testid="stAppViewContainer"] {
            margin-left: 0px !important;
            width: 100% !important;
        }
        """

    # Global static CSS rules
    static_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

        * { font-family: 'Outfit', sans-serif; }

        /* ── App Background ── */
        .stApp {
            background: radial-gradient(circle at top center, #0f172a 0%, #020617 100%) !important;
            color: #f8fafc !important;
        }

        /* ── Hide Streamlit chrome ── */
        #MainMenu, footer, header,
        div[data-testid="stHeader"],
        div[data-testid="stDecoration"],
        div[data-testid="stToolbar"] {
            visibility: hidden !important;
            display: none !important;
        }

        /* ── Hide Sidebar Collapse Controls ── */
        [data-testid="collapsedControl"],
        button[aria-label="Collapse sidebar"],
        [data-testid="stSidebarCollapseButton"],
        button[class*="sidebarCollapse"] {
            display: none !important;
            visibility: hidden !important;
        }

        /* Completely hide scrollbars globally while preserving mouse/touch scrolling */
        ::-webkit-scrollbar {
            display: none !important;
            width: 0px !important;
            height: 0px !important;
            background: transparent !important;
        }
        * {
            -ms-overflow-style: none !important;
            scrollbar-width: none !important;
        }
    """

    # Dynamic styling that follows the conditional styles
    dynamic_css = """
        /* ══════════════════════════════
           SIDEBAR STYLING
        ══════════════════════════════ */
        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #060d1f 0%, #030712 100%) !important;
            border-right: 1px solid rgba(0, 255, 204, 0.07) !important;
            box-shadow: 4px 0 24px rgba(0, 0, 0, 0.6) !important;
        }

        /* Sidebar inner padding */
        section[data-testid="stSidebar"] > div:first-child {
            padding: 1.2rem 1rem !important;
        }

        /* Sidebar horizontal rule */
        section[data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.06) !important;
            margin: 10px 0 !important;
        }

        /* Sidebar widget labels */
        section[data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {
            color: #94a3b8 !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.8px !important;
            margin-bottom: 5px !important;
        }

        /* ── Selectbox trigger (the closed pill) ── */
        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div > div {
            background-color: #0d1424 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            color: #ffffff !important;
            font-size: 0.9rem !important;
            transition: border-color 0.2s ease !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stSelectbox"] > div > div:hover {
            border-color: rgba(0, 255, 204, 0.4) !important;
        }

        /* ── Number input ── */
        section[data-testid="stSidebar"] div[data-baseweb="input"] {
            background-color: #0d1424 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
            border-color: rgba(0, 255, 204, 0.45) !important;
            box-shadow: 0 0 0 2px rgba(0, 255, 204, 0.08) !important;
        }

        section[data-testid="stSidebar"] div[data-baseweb="input"] input {
            color: #ffffff !important;
            background: transparent !important;
            caret-color: #00FFCC !important;
        }

        /* ── Toggle ── */
        section[data-testid="stSidebar"] div[data-testid="stToggle"] label {
            color: #94a3b8 !important;
            font-size: 0.85rem !important;
        }

        /* ── Sidebar buttons ── */
        section[data-testid="stSidebar"] div.stButton > button {
            border-radius: 10px !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            padding: 9px 16px !important;
            width: 100% !important;
            transition: all 0.25s ease !important;
        }

        section[data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #00FFCC 0%, #0099FF 100%) !important;
            color: #020617 !important;
            border: none !important;
            box-shadow: 0 3px 12px rgba(0, 255, 204, 0.2) !important;
        }

        section[data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-primary"]:hover {
            box-shadow: 0 5px 18px rgba(0, 255, 204, 0.35) !important;
            transform: translateY(-1px) !important;
        }

        section[data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            color: #cbd5e1 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }

        section[data-testid="stSidebar"] div.stButton > button[data-testid="baseButton-secondary"]:hover {
            border-color: rgba(239, 68, 68, 0.5) !important;
            color: #f87171 !important;
            background: rgba(239, 68, 68, 0.05) !important;
        }

        /* ── Expander inside sidebar ── */
        section[data-testid="stSidebar"] div[data-testid="stExpander"] {
            background: rgba(255, 255, 255, 0.01) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
        }

        section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
            font-weight: 600 !important;
        }

        /* ══════════════════════════════
           FORM HEADING
        ══════════════════════════════ */
        .form-heading {
            color: #ffffff;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 16px;
            border-left: 3px solid #00FFCC;
            padding-left: 10px;
            letter-spacing: 0.3px;
        }

        /* ══════════════════════════════
           LOGIN CARD
        ══════════════════════════════ */
        .login-card {
            background: linear-gradient(135deg, rgba(30,41,59,0.4) 0%, rgba(15,23,42,0.6) 100%);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 24px;
            padding: 45px 35px;
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.7);
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
        }

        /* ══════════════════════════════
           MAIN CONTENT INPUTS
        ══════════════════════════════ */
        div[data-baseweb="input"] {
            background-color: #0c0f19 !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 12px !important;
            transition: all 0.25s ease !important;
        }

        div[data-baseweb="input"]:focus-within {
            border-color: rgba(0,255,204,0.5) !important;
            box-shadow: 0 0 12px rgba(0,255,204,0.15) !important;
        }

        div[data-baseweb="input"] input {
            background: transparent !important;
            color: #ffffff !important;
            font-size: 0.95rem !important;
            border: none !important;
        }

        div[data-testid="stTextInput"] input,
        div[data-testid="stNumberInput"] input {
            background: transparent !important;
            color: #ffffff !important;
            caret-color: #00FFCC !important;
        }

        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus,
        input:-webkit-autofill:active {
            -webkit-text-fill-color: #ffffff !important;
            -webkit-box-shadow: 0 0 0px 1000px #0c0f19 inset !important;
        }

        div[data-baseweb="input"] input::placeholder { color: #64748b !important; }

        /* ══════════════════════════════
           TABS
        ══════════════════════════════ */
        div.stTabs [data-baseweb="tab-list"] {
            gap: 12px;
            justify-content: center;
            border-bottom: 1px solid rgba(255,255,255,0.05) !important;
        }

        div.stTabs [data-baseweb="tab"] {
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 20px !important;
            padding: 8px 24px !important;
            color: #64748b !important;
            font-weight: 600 !important;
        }

        div.stTabs [data-baseweb="tab"]:hover { color: #ffffff !important; }

        div.stTabs [aria-selected="true"] {
            background: rgba(0,255,204,0.06) !important;
            border-color: rgba(0,255,204,0.3) !important;
            color: #00FFCC !important;
        }

        /* ══════════════════════════════
           HERO BANNER
        ══════════════════════════════ */
        .hero-container {
            background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 30px;
            border: 1px solid rgba(0,255,204,0.08);
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            text-align: center;
        }

        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            background: linear-gradient(90deg, #00FFCC 0%, #0099FF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }

        .hero-subtitle {
            font-size: 1.15rem;
            color: #94a3b8;
            font-weight: 300;
        }

        /* ══════════════════════════════
           CARDS
        ══════════════════════════════ */
        .card {
            background: rgba(255,255,255,0.01);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 16px;
            padding: 24px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: rgba(0,255,204,0.25);
            box-shadow: 0 12px 30px rgba(0,255,204,0.08);
        }

        .card-title { font-size: 1.25rem; font-weight: 600; color: #00FFCC; }
        .card-desc  { font-size: 0.9rem; color: #94a3b8; line-height: 1.5; }

        /* ══════════════════════════════
           STAT CARD
        ══════════════════════════════ */
        .stat-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.02) 0%, rgba(255,255,255,0.005) 100%);
            border: 1px solid rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 14px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.25);
            transition: all 0.3s ease;
        }

        .stat-card:hover {
            border-color: rgba(0,255,204,0.2);
            transform: translateY(-2px);
        }

        /* ══════════════════════════════
           SPEECH BOX
        ══════════════════════════════ */
        .speech-box {
            background: linear-gradient(135deg, rgba(0,255,204,0.02) 0%, rgba(0,153,255,0.02) 100%);
            border: 1px solid rgba(0,255,204,0.15);
            border-radius: 14px;
            padding: 14px;
        }

        /* ══════════════════════════════
           BADGES
        ══════════════════════════════ */
        .status-badge {
            border-radius: 20px; padding: 4px 10px;
            font-size: 0.72rem; font-weight: 700;
            letter-spacing: 0.5px; display: inline-block;
        }

        .badge-completed { background: rgba(0,230,118,0.1); border: 1px solid rgba(0,230,118,0.25); color: #00FF99; }
        .badge-active    { background: rgba(0,255,204,0.1); border: 1px solid rgba(0,255,204,0.35); color: #00FFCC; animation: pulse-active-glow 2s infinite ease-in-out; }
        .badge-pending   { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07); color: #8b949e; }

        @keyframes pulse-active-glow {
            0%   { box-shadow: 0 0 0 0 rgba(0,255,204,0.3); }
            70%  { box-shadow: 0 0 0 5px rgba(0,255,204,0); }
            100% { box-shadow: 0 0 0 0 rgba(0,255,204,0); }
        }

        /* ══════════════════════════════
           GLOBAL BUTTONS
        ══════════════════════════════ */
        div.stButton > button {
            transition: all 0.25s ease !important;
            border-radius: 12px !important;
            font-size: 0.92rem !important;
            padding: 10px 22px !important;
            font-weight: 600 !important;
        }

        div.stButton > button[data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #00FFCC 0%, #0099FF 100%) !important;
            color: #020617 !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(0,255,204,0.15) !important;
        }

        div.stButton > button[data-testid="baseButton-primary"]:hover {
            box-shadow: 0 6px 20px rgba(0,255,204,0.3) !important;
            transform: translateY(-2px) !important;
        }

        div.stButton > button[data-testid="baseButton-secondary"] {
            background: rgba(255,255,255,0.02) !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
        }

        div.stButton > button[data-testid="baseButton-secondary"]:hover {
            border-color: #00FFCC !important;
            color: #00FFCC !important;
        }

        div.stButton > button:active { transform: translateY(0) !important; }

        /* ══════════════════════════════
           DATAFRAME
        ══════════════════════════════ */
        div[data-testid="stDataFrame"] {
            background: rgba(255,255,255,0.01) !important;
            border: 1px solid rgba(255,255,255,0.05) !important;
            border-radius: 12px !important;
            padding: 8px !important;
        }

        /* ══════════════════════════════
           FOOTER
        ══════════════════════════════ */
        .footer {
            text-align: center;
            padding: 25px 0;
            color: #475569;
            font-size: 0.8rem;
            border-top: 1px solid rgba(255,255,255,0.03);
            margin-top: 50px;
        }

        /* ══════════════════════════════
           PROGRESS TABLE ROWS
        ══════════════════════════════ */
        .row-active    { background: rgba(0,255,204,0.02); border-left: 3px solid #00FFCC; }
        .row-completed { opacity: 0.8; }
        .row-pending   { opacity: 0.6; }

    </style>
    """

    script_html = """
    <script>
    /*
     * Kill the search input that Streamlit renders inside every open selectbox.
     * The popover is mounted as a body-level portal (outside #root), so normal
     * st.markdown CSS cannot reach it. We inject a <style> into <head> and
     * watch for new popovers with a MutationObserver.
     */
    (function () {
        var STYLE_ID = '_fitai_no_search';
        if (!document.getElementById(STYLE_ID)) {
            var s = document.createElement('style');
            s.id = STYLE_ID;
            s.textContent =
                '[data-baseweb="popover"] [data-baseweb="input"] { display:none!important; }' +
                '[data-baseweb="popover"] input { display:none!important; }';
            document.head.appendChild(s);
        }

        function hideSearchInputs() {
            document.querySelectorAll(
                '[data-baseweb="popover"] [data-baseweb="input"],' +
                '[data-baseweb="popover"] input'
            ).forEach(function (el) {
                el.style.setProperty('display', 'none', 'important');
            });
        }

        var obs = new MutationObserver(hideSearchInputs);
        obs.observe(document.body, { childList: true, subtree: true });
        hideSearchInputs();
    })();

    /*
     * Auto-expand sidebar if it loads in a collapsed state (e.g. from local storage cache)
     * and clear any remembered collapsed state to prevent layout bugs.
     */
    (function () {
        function forceExpand() {
            // Clear storage keys to prevent remembering collapsed state
            for (var key in localStorage) {
                if (key.toLowerCase().includes('sidebar')) {
                    localStorage.removeItem(key);
                }
            }
            for (var key in sessionStorage) {
                if (key.toLowerCase().includes('sidebar')) {
                    sessionStorage.removeItem(key);
                }
            }
            
            // Re-open if it is collapsed
            var expandBtn = document.querySelector(
                '[data-testid="collapsedControl"], ' +
                '[data-testid="collapsedSidebarOption"], ' +
                'button[aria-label="Expand sidebar"]'
            );
            if (expandBtn) {
                expandBtn.click();
            }
        }
        
        forceExpand();
        var obs = new MutationObserver(forceExpand);
        obs.observe(document.body, { childList: true, subtree: true });
    })();
    </script>
    """

    st.markdown(static_css + layout_css + dynamic_css + script_html, unsafe_allow_html=True)
