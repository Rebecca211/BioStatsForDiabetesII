import streamlit as st
import matplotlib.pyplot as plt
import shap
import numpy as np
from math import pi
import pandas as pd

def render_analytics(df, features, model):
    st.subheader("📊 Personalized Diabetes Risk Insights")
    st.markdown("_Explore how your recent prediction was made._")

    if 'user_input' not in st.session_state or 'user_prediction' not in st.session_state:
        st.info("👈 Please predict first using the 'Predict' tab.")
        return

    user_input = st.session_state['user_input']
    user_array = np.array(list(user_input.values())).reshape(1, -1)
    user_prob = st.session_state['user_prediction']['prob']

    explainer = shap.Explainer(model, df[features])
    shap_values = explainer(df[features])
    user_shap = explainer(user_array)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Comparison Chart",
        "🧠 SHAP Explanation",
        "🧬 Radar Profile",
        "🎯 Risk Score",
        "📋 Summary",
        "🧪 Feature Impact Tester"
    ])

    with tab1:
        st.markdown("### 📊 Your Features vs Population Averages")
        try:
            labels = list(user_input.keys())
            your_vals = list(user_input.values())
            non_diabetic_avg = df[df["Outcome"] == 0][features].mean().values
            diabetic_avg = df[df["Outcome"] == 1][features].mean().values
            x = np.arange(len(labels))
            width = 0.25
            fig, ax = plt.subplots(figsize=(10, 5))
            bars1 = ax.bar(x - width, your_vals, width, label="You")
            bars2 = ax.bar(x, non_diabetic_avg, width, label="Non-Diabetic Avg")
            bars3 = ax.bar(x + width, diabetic_avg, width, label="Diabetic Avg")
            for bars in [bars1, bars2, bars3]:
                for bar in bars:
                    height = bar.get_height()
                    ax.annotate(f'{height:.0f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                                xytext=(0, 3), textcoords="offset points",
                                ha='center', va='bottom', fontsize=8)
            ax.set_ylabel("Value")
            ax.set_title("Feature Comparison")
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45)
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"❌ Error rendering comparison chart: {e}")

    with tab2:
        st.markdown("### 🧠 SHAP Explanation")
        try:
            fig, ax = plt.subplots()
            shap.plots.waterfall(user_shap[0], show=False)
            st.pyplot(plt.gcf())
            plt.clf()
        except Exception as e:
            st.error(f"❌ Error rendering SHAP plot: {e}")

    with tab3:
        st.markdown("### 🧬 Risk Profile Radar")
        try:
            norm_df = (df[features] - df[features].min()) / (df[features].max() - df[features].min())
            user_row = np.array(list(user_input.values()))
            norm_user = (user_row - df[features].min().values) / (df[features].max().values - df[features].min().values)
            values = norm_user.tolist() + [norm_user[0]]
            angles = [n / float(len(features)) * 2 * pi for n in range(len(features))] + [0]
            fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
            ax.plot(angles, values, linewidth=2, linestyle='solid', label="Your Input", color="#FF4B4B")
            ax.fill(angles, values, color="#FF9999", alpha=0.25)
            ax.set_theta_offset(pi / 2)
            ax.set_theta_direction(-1)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(features, fontsize=10, fontweight='bold')
            ax.set_yticklabels(["Low", "Medium", "High"], fontsize=8)
            ax.set_title("🧬 Risk Profile Radar", size=16, color="#333", pad=20)
            ax.grid(True, color="#DDDDDD")
            ax.spines["polar"].set_visible(False)
            ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
            st.pyplot(fig)
            plt.close(fig)
        except Exception as e:
            st.error(f"❌ Error rendering radar chart: {e}")

    with tab4:
        st.markdown("### 🎯 Your Risk Score")
        st.markdown("_This score reflects how likely the model thinks you are at risk._")
        st.markdown(f"""
        <div style="background-color:#f0f0f0; border-radius:8px; padding:6px; margin:10px 0;">
          <div style="width:{user_prob*100:.1f}%; background-color:#e74c3c;
                      padding:10px; border-radius:6px; color:white; text-align:center;">
            Your Risk Score: {user_prob*100:.1f}%
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("### 🚦 Risk Threshold Interpretation")
        if user_prob >= 0.7:
            st.error("🟥 High Risk: Above 70%")
        elif user_prob >= 0.4:
            st.warning("🟧 Moderate Risk: Between 40% and 70%")
        else:
            st.success("🟩 Low Risk: Below 40%")

    with tab5:
        st.markdown("### 📋 Input Summary")
        st.json(user_input)
        st.info("✅ These values were used in your prediction.")

    with tab6:
        st.markdown("### 🧪 Feature Impact Tester")
        st.markdown("_Use sliders below to test how changing your values impacts the risk score._")
        test_input = {}
        for feature in features:
            val = st.slider(feature, float(df[feature].min()), float(df[feature].max()), float(user_input[feature]))
            test_input[feature] = val

        test_array = np.array(list(test_input.values())).reshape(1, -1)
        test_prob = model.predict_proba(test_array)[0][1]
        st.metric(label="Predicted Risk with Adjusted Inputs", value=f"{test_prob*100:.1f}%")

        if test_prob >= 0.7:
            st.error("🟥 High Risk")
        elif test_prob >= 0.4:
            st.warning("🟧 Moderate Risk")
        else:
            st.success("🟩 Low Risk")

    st.markdown("---")
    st.markdown("📘 **Disclaimer:**")
    st.markdown("""
    This risk score is based on a machine learning model trained on population data.
    It reflects statistical probability — not a clinical diagnosis.
    For medical concerns, always consult a qualified healthcare provider.
    """)