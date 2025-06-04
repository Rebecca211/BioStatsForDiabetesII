# diabetes_charts.py

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Set Streamlit page config
st.set_page_config(layout="wide")
st.title("Diabetes Risk Analysis Dashboard")

# Load dataset
df = pd.read_csv("diabetes.csv")

# Data cleaning
features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
df[features] = df[features].replace(0, np.nan)
df[features] = df[features].fillna(df[features].median())

# Binning
df["BMICategory"] = pd.cut(df["BMI"], bins=[0, 18.5, 25, 30, 35, 50],
                           labels=["Underweight", "Normal", "Overweight", "Obese I", "Obese II"])
df["AgeGroup"] = pd.cut(df["Age"], bins=[20, 30, 40, 50, 60, 80],
                        labels=["20s", "30s", "40s", "50s", "60+"])

# BMI vs Diabetes Rate
fig1 = px.bar(
    df.groupby("BMICategory", observed=True)["Outcome"].mean().reset_index(),
    x="BMICategory", y="Outcome", title="Diabetes Rate by BMI Category",
    labels={"Outcome": "Diabetes Rate"}
)
st.plotly_chart(fig1, use_container_width=True)

# Age Group vs Diabetes Rate
fig2 = px.bar(
    df.groupby("AgeGroup", observed=True)["Outcome"].mean().reset_index(),
    x="AgeGroup", y="Outcome", title="Diabetes Rate by Age Group",
    labels={"Outcome": "Diabetes Rate"}
)
st.plotly_chart(fig2, use_container_width=True)

# Pregnancies vs Diabetes Rate
preg_stats = df.groupby("Pregnancies")["Outcome"].mean().reset_index()
fig3 = px.scatter(preg_stats, x="Pregnancies", y="Outcome", title="Diabetes Rate by Pregnancies")
fig3.add_trace(go.Scatter(x=preg_stats["Pregnancies"], y=preg_stats["Outcome"], mode='lines'))
st.plotly_chart(fig3, use_container_width=True)

# 3D Risk Plot
fig4 = px.scatter_3d(df, x="Age", y="BMI", z="Pregnancies", color="Outcome",
                     title="3D Risk View", color_continuous_scale="RdBu")
st.plotly_chart(fig4)

# Heatmap of Age x BMI vs Diabetes
df['AgeBin'] = pd.cut(df['Age'], bins=[20,30,40,50,60,70], labels=['20s','30s','40s','50s','60s'])
df['BMIBin'] = pd.cut(df['BMI'], bins=[0,18.5,25,30,35,50], labels=['Underweight','Normal','Overweight','Obese I','Obese II'])
pivot = df.pivot_table(index="BMIBin", columns="AgeBin", values="Outcome", aggfunc="mean")

st.subheader("Heatmap: Diabetes Rate by Age and BMI")
plt.figure(figsize=(8, 6))

sns.heatmap(pivot, annot=True, cmap="YlOrRd", fmt=".2f")
plt.title("Diabetes Rate Heatmap by Age and BMI")
st.pyplot(plt.gcf())
plt.close()
