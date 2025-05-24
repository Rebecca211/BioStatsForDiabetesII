import streamlit as st

def render_recommendation(probability):
    st.subheader("📌 Personalized Recommendations")
    st.markdown("_Lifestyle and wellness tips based on your risk level._")

    if probability >= 0.7:
        st.error("🟥 **High Risk**: You may be at significant risk of diabetes.")
        st.markdown("""
        - ✅ **Consult a healthcare provider** immediately for a full diagnostic assessment.
        - 🥦 Adopt a **low-sugar, high-fiber diet** (e.g., whole grains, legumes, veggies).
        - 🚶‍♂️ **Exercise daily** (e.g., brisk walking 30+ minutes).
        - 🧂 Reduce sodium and processed food intake.
        - 📉 Track **weight, glucose, and BMI** weekly.
        """)
    elif probability >= 0.4:
        st.warning("🟧 **Moderate Risk**: You show some signs of elevated risk.")
        st.markdown("""
        - 🍽 Maintain a **balanced diet** with controlled carbs and sugars.
        - 🏃‍♂️ Include **150 mins/week of moderate activity** (walking, cycling, swimming).
        - 🩺 Consider **regular screenings** (e.g., fasting glucose tests).
        - 📓 Start a **health log**: diet, sleep, weight, energy.
        """)
    else:
        st.success("🟩 **Low Risk**: You are currently within a healthy range.")
        st.markdown("""
        - 🥗 Keep up healthy habits (plant-based meals, hydration).
        - 🚶‍♀️ Continue physical activity (even light: walking, yoga, stretching).
        - 📊 Reassess every 6–12 months or if symptoms arise.
        - ✅ Encourage peers to screen and stay proactive.
        """)

    st.info("These are general lifestyle guidelines and not a substitute for medical advice.")