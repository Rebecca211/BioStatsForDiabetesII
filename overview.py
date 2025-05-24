import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def render_overview(df):
    st.markdown("<h2 style='text-align: center;'>🧬 Diabetes Risk Analytics Dashboard</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Explore key insights, risk indicators, and filtered breakdowns of the dataset.</p>", unsafe_allow_html=True)

    # Filter by Age Group
    age_bins = pd.cut(df["Age"], bins=[0, 20, 30, 40, 50, 60, 70, 100], right=False)
    df["AgeGroup"] = age_bins.astype(str)
    with st.expander("🎚️ Filter: Select Age Group"):
        selected_age_group = st.selectbox("Choose Age Group", options=sorted(df["AgeGroup"].unique()))
    filtered_df = df[df["AgeGroup"] == selected_age_group]

    diabetes_pct = filtered_df['Outcome'].mean() * 100 if len(filtered_df) > 0 else 0

    # KPIs
    st.markdown("### 📌 Key Metrics")
    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric("👥 Group Size", len(filtered_df))
    with kpi2:
        st.metric("🩺 Diabetes Rate", f"{diabetes_pct:.1f}%")
    with kpi3:
        st.metric("🧪 Avg Glucose", f"{filtered_df['Glucose'].mean():.1f}")

    # Gauge
    st.markdown("### 🧭 Diabetes Risk Gauge")
    fig, ax = plt.subplots(figsize=(4, 2), dpi=120)
    ax.axis("equal")
    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-0.2, 1.2)
    ax.axis("off")
    wedge_colors = ['#28a745', '#ffc107', '#dc3545']
    ax.pie([40, 30, 30], startangle=180, colors=wedge_colors, radius=1.0)
    angle = 180 + (diabetes_pct / 100) * 180
    ax.annotate('', xy=(0.85 * np.cos(np.radians(angle)), 0.85 * np.sin(np.radians(angle))), xytext=(0, 0),
                arrowprops=dict(facecolor='black', shrink=0.05, width=2, headwidth=8))
    ax.text(0, -0.1, f"{diabetes_pct:.1f}%", ha='center', fontsize=12, fontweight='bold')
    ax.text(-1, -0.2, 'Low', fontsize=9, color='#28a745')
    ax.text(0, -0.3, 'Moderate', fontsize=9, color='#ffc107')
    ax.text(1, -0.2, 'High', fontsize=9, color='#dc3545')
    st.pyplot(fig)

    # Charts
    with st.container():
        row1 = st.columns(2)
        with row1[0]:
            st.markdown("### 👥 Outcome Distribution")
            fig1, ax1 = plt.subplots()
            filtered_df['Outcome'].value_counts().plot(kind='bar', color=['#1f77b4', '#ff7f0e'], ax=ax1)
            ax1.set_xticks([0, 1])
            ax1.set_xticklabels(['No Diabetes', 'Diabetes'])
            ax1.set_ylabel("Count")
            st.pyplot(fig1)

        with row1[1]:
            st.markdown("### 📊 Glucose Distribution")
            fig2, ax2 = plt.subplots()
            sns.histplot(data=filtered_df, x="Glucose", hue="Outcome", kde=True, palette="Set2", ax=ax2)
            st.pyplot(fig2)

    row2 = st.columns(2)
    with row2[0]:
        st.markdown("### 📦 BMI Boxplot")
        fig3, ax3 = plt.subplots()
        sns.boxplot(x="Outcome", y="BMI", data=filtered_df, palette="pastel", ax=ax3)
        st.pyplot(fig3)

    with row2[1]:
        st.markdown("### 🔗 Feature Correlation")
        fig4, ax4 = plt.subplots(figsize=(6, 5))
        sns.heatmap(filtered_df.select_dtypes(include="number").corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax4)
        st.pyplot(fig4)

    st.markdown("### 🧬 Feature Distributions")
    dist_cols = st.columns(3)
    for i, feat in enumerate(['BloodPressure', 'Insulin', 'SkinThickness']):
        with dist_cols[i]:
            fig, ax = plt.subplots()
            sns.histplot(data=filtered_df, x=feat, kde=True, ax=ax, color='#007acc')
            ax.set_title(f"{feat}")
            st.pyplot(fig)

    st.markdown("### 📋 Descriptive Statistics")
    st.dataframe(filtered_df.describe().T.style.format("{:.1f}"))

    st.markdown("<p style='text-align:center;'>All visualizations reflect filtered data for <b>age group</b>.</p>", unsafe_allow_html=True)