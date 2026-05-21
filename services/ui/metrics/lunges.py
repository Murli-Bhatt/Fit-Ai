import streamlit as st

def render_lunge_metrics(angles):
    """
    Renders visual indicators and posture logs specific to Lunges.
    """
    front_knee = angles.get("front_knee", 170.0)
    back_knee = angles.get("back_knee", 165.0)
    
    # Calculate lunging depth status based on front knee flexion
    if front_knee <= 95:
        depth = "Deep Lunge (Excellent)"
        depth_color = "#00FFCC"
    elif front_knee <= 120:
        depth = "Partial Flexion (Lunge Deeper)"
        depth_color = "#FFA500"
    else:
        depth = "Standing / Rest State"
        depth_color = "#9ca3af"

    # Analyze back knee clearance
    if back_knee <= 80:
        clearance = "Warning: Back Knee Too Close to Floor!"
        clearance_color = "#FF3366"
    elif back_knee <= 105:
        clearance = "Perfect Back Knee Position (~90°)"
        clearance_color = "#00FFCC"
    else:
        clearance = "Awaiting Lowering Phase"
        clearance_color = "#9ca3af"

    st.markdown("<h4 style='color: #00FFCC; font-weight: 600; margin-bottom: 12px;'>🏃 Lunge Biometrics</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Front Knee</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{front_knee:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #00FFCC; width: {min(100, int((front_knee/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Target: ~90° in lunge</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Back Knee</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{back_knee:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #0099FF; width: {min(100, int((back_knee/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Target: ~90° (off ground)</div>
        </div>
        """, unsafe_allow_html=True)

    # Posture alerts
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {depth_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Lunge Depth Status</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{depth}</div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {clearance_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Back Leg Alignment</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{clearance}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
