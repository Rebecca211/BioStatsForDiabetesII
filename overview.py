import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.stats.proportion import proportion_confint


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

    # --- Bar & Pie Charts Row ---
    col_bar, col_pie = st.columns(2)

    fig_outcome = px.histogram(df, x="Outcome", color="Outcome", barmode="group",
                               color_discrete_map={0: '#2b7bba', 1: '#e74c3c'},
                               labels={"Outcome": "Diabetes Status"},
                               category_orders={"Outcome": [0, 1]})
    fig_outcome.update_layout(title="Outcome Count", height=300, xaxis_title="", yaxis_title="Count", showlegend=False)

    pie_data = df["Outcome"].value_counts().rename({0: "No Diabetes", 1: "Diabetes"})
    fig_pie = px.pie(pie_data, values=pie_data.values, names=pie_data.index,
                     color=pie_data.index,
                     color_discrete_map={"No Diabetes": "#27ae60", "Diabetes": "#e74c3c"})
    fig_pie.update_layout(title="Outcome Ratio", height=300)

    with col_bar:
        st.plotly_chart(fig_outcome, use_container_width=True)
    with col_pie:
        st.plotly_chart(fig_pie, use_container_width=True)

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
    st.markdown("#### 📈 Diabetes Rate Trends")

    age_bins = [20, 30, 40, 50, 100]
    age_labels = ["20-29", "30-39", "40-49", "50+"]
    df["AgeGroup"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=True, include_lowest=True)
    age_diabetes_rate = df.groupby("AgeGroup")["Outcome"].agg(['mean', 'count', 'sum']).reset_index()
    age_diabetes_rate.columns = ["AgeGroup", "DiabetesRate", "SampleSize", "NumDiabetes"]

    # Compute 95% Confidence Interval
    age_diabetes_rate['CI_lower'], age_diabetes_rate['CI_upper'] = proportion_confint(
        count=age_diabetes_rate['NumDiabetes'],
        nobs=age_diabetes_rate['SampleSize'],
        alpha=0.05,
        method='wilson')

    fig_age = px.line(age_diabetes_rate, x="AgeGroup", y="DiabetesRate", markers=True, title="By Age Group",
                      error_y=age_diabetes_rate['CI_upper'] - age_diabetes_rate['DiabetesRate'],
                      error_y_minus=age_diabetes_rate['DiabetesRate'] - age_diabetes_rate['CI_lower'])
    fig_age.update_traces(line=dict(color='green', width=3))

    pregnancy_stats = df.groupby("Pregnancies")["Outcome"].mean().reset_index()
    pregnancy_stats.rename(columns={"Outcome": "DiabetesRate"}, inplace=True)
    fig_preg = px.line(pregnancy_stats, x="Pregnancies", y="DiabetesRate", markers=True, title="By Pregnancies")

    bmi_bins = [0, 18.5, 25, 30, 35, 50, 70]
    bmi_labels = ["Underweight", "Normal", "Overweight", "Obese I", "Obese II", "Severe Obese"]
    df["BMICategory"] = pd.cut(df["BMI"], bins=bmi_bins, labels=bmi_labels, right=False)
    bmi_diabetes_rate = df.groupby("BMICategory")["Outcome"].mean().reset_index()
    bmi_diabetes_rate.rename(columns={"Outcome": "DiabetesRate"}, inplace=True)
    fig_bmi = px.line(bmi_diabetes_rate, x="BMICategory", y="DiabetesRate", markers=True, title="By BMI Category")
    fig_bmi.update_traces(line=dict(color='orange', width=3))

    row1, row2, row3 = st.columns(3)
    with row1:
        st.plotly_chart(fig_age, use_container_width=True)
    with row2:
        st.plotly_chart(fig_preg, use_container_width=True)
    with row3:
        st.plotly_chart(fig_bmi, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🌐 3D Risk Views")

    col1, col2, col3 = st.columns(3)

    with col1:
        df["DiabetesLabel"] = df["Outcome"].map({0: "No Diabetes", 1: "Diabetes"})
        fig_3d = px.scatter_3d(df, x="Age", y="BMI", z="Pregnancies", color="DiabetesLabel",
                               color_discrete_map={"No Diabetes": "#2c3e50", "Diabetes": "#e74c3c"},
                               opacity=0.7, size_max=5, title="Age, BMI, Pregnancies")
        fig_3d.update_layout(scene=dict(xaxis_title="Age", yaxis_title="BMI", zaxis_title="Pregnancies", aspectmode='cube'))
        st.plotly_chart(fig_3d, use_container_width=True)

    with col2:
        df['AgeBin'] = pd.cut(df['Age'], bins=np.arange(20, 80, 10))
        df['BMIBin'] = pd.cut(df['BMI'], bins=np.arange(15, 50, 5))
        pivot_table = df.pivot_table(index='AgeBin', columns='BMIBin', values='Outcome', aggfunc='mean')
        fig_surface = go.Figure(data=[go.Surface(
            z=pivot_table.values,
            x=[str(i) for i in pivot_table.columns],
            y=[str(i) for i in pivot_table.index],
            colorscale='Viridis')])
        fig_surface.update_layout(title="Surface: Age & BMI",
                                  scene=dict(xaxis_title="BMI", yaxis_title="Age", zaxis_title="Rate"))
        st.plotly_chart(fig_surface, use_container_width=True)

    with col3:
        df['GlucoseBin'] = pd.cut(df['Glucose'], bins=np.arange(50, 200, 20))
        df['AgeBin'] = pd.cut(df['Age'], bins=np.arange(20, 80, 10))
        pivot_gluc = df.pivot_table(index='AgeBin', columns='GlucoseBin', values='Outcome', aggfunc='mean')
        fig_gluc = go.Figure(data=[go.Surface(
            z=pivot_gluc.values,
            x=[str(i) for i in pivot_gluc.columns],
            y=[str(i) for i in pivot_gluc.index],
            colorscale='Plasma')])
        fig_gluc.update_layout(title="Surface: Age & Glucose",
                               scene=dict(xaxis_title="Glucose", yaxis_title="Age", zaxis_title="Rate"))
        st.plotly_chart(fig_gluc, use_container_width=True)
        
    with st.expander("📋 View Summary Statistics"):
        styled_df = df.describe().T.style.background_gradient(cmap="PuBu")
        st.dataframe(styled_df, height=350)

