import streamlit as st
import numpy as np
import qrcode
from io import BytesIO
from streamlit_lottie import st_lottie
import json
from recommendation import render_recommendation

def load_lottie(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def render_predict(df, features, model):
    st.markdown("## 🔬 Diabetes Risk Prediction")

    bounds = {
        "Glucose": (50.0, 300.0),
        "BloodPressure": (40.0, 200.0),
        "SkinThickness": (7.0, 99.0),
        "Insulin": (15.0, 900.0),
        "BMI": (10.0, 70.0),
        "Age": (1.0, 120.0)
    }

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("### 📝 Patient Data")
        with st.form("manual_input_form"):
            manual_input = {}
            cols = st.columns(2)
            for i, feature in enumerate(features):
                min_val, max_val = bounds.get(feature, (0.0, 9999.0))
                with cols[i % 2]:
                    manual_input[feature] = st.number_input(
                        label=feature,
                        value=float(df[feature].median()),
                        min_value=min_val,
                        max_value=max_val,
                        format="%.1f"
                    )
            submitted = st.form_submit_button("🚀 Predict")

    if submitted:
        invalid_fields = [f for f in features if not bounds[f][0] <= manual_input[f] <= bounds[f][1]]
        if invalid_fields:
            st.warning("🚫 Some input values are outside expected ranges.")
            st.markdown(f"**Check fields:** {', '.join(invalid_fields)}")
            return

        # Store in session state
        st.session_state['user_input'] = manual_input

        manual_array = np.array(list(manual_input.values())).reshape(1, -1)
        manual_prob = model.predict_proba(manual_array)[0][1]
        manual_class = model.predict(manual_array)[0]
        st.session_state['user_prediction'] = {
            'class': manual_class,
            'prob': manual_prob
        }

        result_col1, result_col2 = st.columns([1, 1])
        with result_col1:
            st.markdown("### 🧠 Result")
            st.metric("Prediction", "🩺 Diabetes" if manual_class else "✅ No Diabetes", f"{manual_prob*100:.1f}%")
            st.markdown(f"""
            <div style="background-color:#f0f0f0; border-radius:6px; padding:2px; margin: 5px 0;">
              <div style="width:{manual_prob*100:.1f}%; background-color:#007aff;
                          padding:6px; border-radius:5px; color:white; text-align:center; font-size:small;">
                Confidence: {manual_prob*100:.1f}%
              </div>
            </div>
            """, unsafe_allow_html=True)

        with result_col2:
            if manual_prob >= 0.7:
                st.error("🟥 High Risk")
                st_lottie(load_lottie("high_risk.json"), height=140)
            elif manual_prob >= 0.4:
                st.warning("🟧 Moderate Risk")
                st_lottie(load_lottie("medium_risk.json"), height=140)
            else:
                st.success("🟩 Low Risk")
                st_lottie(load_lottie("low_risk.json"), height=140)

      

        # QR code
        st.markdown("### 📱 On Your Phone")
        app_url = "https://your-app-url.streamlit.app"
        qr_img = qrcode.make(app_url)
        buf = BytesIO()
        qr_img.save(buf, format="PNG")
        st.image(buf.getvalue(), caption="Scan this QR", width=180)
        st.markdown("___")
        st.markdown("🧬 _AI analysis based on input health metrics._")