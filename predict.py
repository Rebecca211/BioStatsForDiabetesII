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
        "Insulin": (15.0, 900.0),
        "BMI": (10.0, 70.0),
        "Age": (1.0, 120.0)
    }

    # Create two side-by-side columns
    col_form, col_result = st.columns([1.2, 1])

    with col_form:
        st.markdown("### 📝 Patient Data")
        with st.form("manual_input_form"):
            manual_input = {}
            cols = st.columns(2)
            for i, feature in enumerate(features):
                min_val, max_val = bounds.get(feature, (0.0, 9999.0))
                with cols[i % 2]:
                    # Remove stepper (+/-) by using text_input with float conversion
                    user_val = st.text_input(
                        label=f"{feature} ({min_val}-{max_val})",
                        value=f"{df[feature].median():.1f}",
                        key=feature
                    )
                    try:
                        val = float(user_val)
                        manual_input[feature] = val
                    except ValueError:
                        manual_input[feature] = None  # Invalid input for now

            submitted = st.form_submit_button("🚀 Predict")

    if submitted:
        # Validation
        invalid_fields = [
            f for f in features
            if manual_input[f] is None or not bounds[f][0] <= manual_input[f] <= bounds[f][1]
        ]
        if invalid_fields:
            st.warning("🚫 Some input values are missing or out of bounds.")
            st.markdown(f"**Check fields:** {', '.join(invalid_fields)}")
            return

        # Store input in session state
        st.session_state['user_input'] = manual_input

        manual_array = np.array(list(manual_input.values())).reshape(1, -1)
        manual_prob = model.predict_proba(manual_array)[0][1]
        manual_class = model.predict(manual_array)[0]
        st.session_state['user_prediction'] = {
            'class': manual_class,
            'prob': manual_prob
        }

        # Show result in right column
        with col_result:
            st.markdown("### 🧠 Prediction Result")
            st.metric( "","🩺 Diabetes" if manual_class else "✅ No Diabetes", f"{manual_prob*100:.1f}%")

            st.markdown(f"""
            <div style="background-color:#f0f0f0; border-radius:6px; padding:2px; margin: 5px 0;">
              <div style="width:{manual_prob*100:.1f}%; background-color:#007aff;
                          padding:6px; border-radius:5px; color:white; text-align:center; font-size:small;">
                Risk of Diabetes: {manual_prob*100:.1f}%
              </div>
            </div>
            """, unsafe_allow_html=True)

            if manual_prob >= 0.7:
                st.error("🟥 High Risk")
                st_lottie(load_lottie("high_risk.json"), height=120)
            elif manual_prob >= 0.4:
                st.warning("🟧 Moderate Risk")
                st_lottie(load_lottie("medium_risk.json"), height=120)
            else:
                st.success("🟩 Low Risk")
                st_lottie(load_lottie("low_risk.json"), height=120)

            st.markdown("### 📱 Scan for Mobile")
            app_url = "https://biostatsfordiabetesii.streamlit.app/"
            qr_img = qrcode.make(app_url)
            buf = BytesIO()
            qr_img.save(buf, format="PNG")
            st.image(buf.getvalue(), caption="Open on Phone", width=160)
            st.markdown("_AI-based prediction from clinical metrics._")
