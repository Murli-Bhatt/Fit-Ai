import streamlit as st

def render_plank_metrics(angles):
    """
    Renders visual indicators and posture logs specific to Planks.
    """
    hip = angles.get("hip", 178.0)
    elbow = angles.get("elbow", 90.0)
    
    # Calculate hip alignment status (Plank requires flat torso, ~170-185 range)
    if 170 <= hip <= 186:
        hip_status = "Perfect Alignment (Flat Back)"
        hip_color = "#00FFCC"
    elif hip < 170:
        hip_status = "Hips Sagging (Engage your Core!)"
        hip_color = "#FF3366"
    else:
        hip_status = "Hips Elevated (Lower your Glutes)"
        hip_color = "#FFA500"

    # Elbow angle check
    if 80 <= elbow <= 100:
        elbow_status = "Optimal Elbow Angle (~90°)"
        elbow_color = "#00FFCC"
    else:
        elbow_status = "Adjust elbows below shoulders"
        elbow_color = "#FFA500"

    st.markdown("<h4 style='color: #00FFCC; font-weight: 600; margin-bottom: 12px;'>🧘 Plank Biometrics</h4>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Hip Alignment</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{hip:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #00FFCC; width: {min(100, int((hip/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Optimal range: 170° - 185°</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Elbow Joint</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; margin: 5px 0;">{elbow:.1f}°</div>
            <div style="background: rgba(255, 255, 255, 0.05); height: 6px; border-radius: 3px; overflow: hidden;">
                <div style="background: #0099FF; width: {min(100, int((elbow/180)*100))}%; height: 100%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 4px;">Target: ~90° shoulder stack</div>
        </div>
        """, unsafe_allow_html=True)

    # Posture alerts
    st.markdown(f"""
    <div style="margin-top: 15px; display: flex; flex-direction: column; gap: 10px;">
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {hip_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Hip Positioning</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{hip_status}</div>
        </div>
        <div style="background: rgba(255, 255, 255, 0.02); border-left: 4px solid {elbow_color}; border-radius: 4px 12px 12px 4px; padding: 12px; border-top: 1px solid rgba(255, 255, 255, 0.05); border-right: 1px solid rgba(255, 255, 255, 0.05); border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
            <div style="font-size: 0.8rem; color: #9ca3af; font-weight: 600;">Skeletal Geometry</div>
            <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin-top: 3px;">{elbow_status}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
