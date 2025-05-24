
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

def render_overview(df):
    st.markdown("## 📊 Diabetes Dashboard Overview")
    st.markdown("#### _Understand the population distribution, outcomes, and clinical patterns._")

    features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Age']

    # --- Metrics Row ---
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric("👥 Total Patients", f"{len(df)}")
    with kpi2:
        st.metric("💉 Diabetes Rate", f"{df['Outcome'].mean()*100:.1f}%")
    with kpi3:
        st.metric("🧪 Avg Glucose", f"{df['Glucose'].mean():.1f}")
    with kpi4:
        st.metric("📏 Avg BMI", f"{df['BMI'].mean():.1f}")

    st.markdown("---")

    # --- Charts: Outcome Count and Ratio ---
    c1, c2 = st.columns([1.3, 1])
    with c1:
        st.markdown("#### 📊 Outcome Count")
        fig_outcome = px.histogram(df, x="Outcome", color="Outcome", barmode="group",
                                   color_discrete_map={0: '#2b7bba', 1: '#e74c3c'},
                                   labels={"Outcome": "Diabetes Status"},
                                   category_orders={"Outcome": [0, 1]})
        fig_outcome.update_layout(height=300, xaxis_title="", yaxis_title="Count", showlegend=False)
        fig_outcome.update_xaxes(tickvals=[0, 1], ticktext=["No Diabetes", "Diabetes"])
        st.plotly_chart(fig_outcome, use_container_width=True)

    with c2:
        st.markdown("#### 🧁 Outcome Ratio")
        pie_data = df["Outcome"].value_counts().rename({0: "No Diabetes", 1: "Diabetes"})
        fig_pie = px.pie(pie_data, values=pie_data.values, names=pie_data.index,
                         color=pie_data.index,
                         color_discrete_map={"No Diabetes": "#27ae60", "Diabetes": "#e74c3c"})
        fig_pie.update_layout(height=300, showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- Interactive Slider for Glucose vs Age Group ---
    st.markdown("#### 🎯 Glucose vs Age by Age Group")

    age_bins = [20, 30, 40, 50, 60, 70, 90]
    age_labels = ['20-29', '30-39', '40-49', '50-59', '60-69', '70+']
    df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=False)

    selected_group = st.select_slider(
        "Select Age Group:",
        options=age_labels,
        value=age_labels[2]
    )

    filtered_df = df[df["AgeGroup"] == selected_group]

    fig_slider = px.scatter(
        filtered_df,
        x="Age",
        y="Glucose",
        color="Outcome",
        title=f"🧪 Glucose Levels for Age Group {selected_group}",
        color_discrete_sequence=["#2ca02c", "#d62728"],
        labels={"Outcome": "Diabetes"},
        height=500
    )

    st.plotly_chart(fig_slider, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 📦 Feature Distributions")

    dist1, dist2, dist3 = st.columns(3)
    with dist1:
        fig1 = px.histogram(df, x="Glucose", color="Outcome", nbins=40,
                            color_discrete_sequence=["#1f77b4", "#ff7f0e"])
        fig1.update_layout(title="Glucose Distribution", height=250)
        st.plotly_chart(fig1, use_container_width=True)
    with dist2:
        fig2 = px.histogram(df, x="BMI", color="Outcome", nbins=40,
                            color_discrete_sequence=["#1f77b4", "#ff7f0e"])
        fig2.update_layout(title="BMI Distribution", height=250)
        st.plotly_chart(fig2, use_container_width=True)
    with dist3:
        fig3 = px.histogram(df, x="Insulin", color="Outcome", nbins=40,
                            color_discrete_sequence=["#1f77b4", "#ff7f0e"])
        fig3.update_layout(title="Insulin Distribution", height=250)
        st.plotly_chart(fig3, use_container_width=True)

    st.markdown("---")

    # --- Summary Table ---
    st.markdown("#### 📋 Summary Statistics")
    styled_df = df.describe().T.style.background_gradient(cmap="PuBu")
    st.dataframe(styled_df, height=350)
