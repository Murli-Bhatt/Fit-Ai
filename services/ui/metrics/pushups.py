import streamlit as st

def render_pushup_metrics(angles):
    """
    Renders visual indicators and alignment logs specific to Push-ups.
    """
    elbow = angles.get("elbow", 175.0)
    torso = angles.get("torso", 178.0)
    
    # Calculate depth status based on elbow flexion
    if elbow <= 90:
        depth = "Excellent (Chest to Floor)"
        depth_color = "#00FFCC"
    elif elbow <= 120:
        depth = "Moderate Depth (Go Deeper)"
        depth_color = "#FFA500"
    else:
        depth = "Top Plank / Starting"
        depth_color = "#9ca3af"

    # Calculate torso rigidity status based on hip/back line angle (should be straight ~170-180)
    if torso < 165:
        torso_status = "Sagging Hips (Tighten Core!)"
        torso_color = "#FF3366"
    elif torso > 190:
        torso_status = "High Hips / Pike (Keep Body Straight)"
        torso_color = "#FF3366"
    else:
        torso_status = "Excellent Rigid Torso"
        torso_color = "#00FFCC"

    st.markdown("<h4 style='color: #00FFCC; font-weight: 600; margin-bottom: 12px;'>💪 Push-up Biometrics</h4>", unsafe_allow_html=True)
    
    # Grid of gauges
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Elbow Flexion</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{elbow:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #00FFCC; width: {min(100, int((elbow/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Target: ≤ 90° for full depth</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Torso Rigidity</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{torso:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #0099FF; width: {min(100, int((torso/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Target: ~180° straight alignment</div>
        </div>
        """, unsafe_allow_html=True)

    # Posture alerts
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {depth_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Push-up Depth</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{depth}</div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {torso_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Core/Torso Alignment</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{torso_status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
