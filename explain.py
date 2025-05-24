import streamlit as st
import shap
import matplotlib.pyplot as plt

def render_explain(df, features, model):
    st.subheader("🧠 Model Explainability with SHAP")
    X = df[features]
    explainer = shap.Explainer(model, X)
    shap_values = explainer(X)

    st.markdown("### 🔍 Global Feature Importance")
    fig_summary, ax_summary = plt.subplots()
    shap.plots.beeswarm(shap_values, max_display=6, show=False)
    st.pyplot(fig_summary)

    st.markdown("### 👤 Explain Individual Prediction")
    patient_index = st.slider("Select Patient Index", 0, len(df)-1, 0)
    st.write("**Prediction:**", "Diabetes" if model.predict(X.iloc[[patient_index]])[0] else "No Diabetes")
    st.write("**Probability:**", f"{model.predict_proba(X.iloc[[patient_index]])[0][1] * 100:.1f}%")

    fig_force, ax = plt.subplots()
    plt.sca(ax)
    shap.plots.waterfall(shap_values[patient_index], show=False)
    st.pyplot(fig_force)