import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from streamlit_option_menu import option_menu

# Page config
st.set_page_config(
    page_title="🧬 Advanced Diabetes Risk Dashboard",
    page_icon="💡",
    layout="wide"
)

# Custom header with styling
st.markdown(
    """
    <style>
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    .css-1rs6os.edgvbvh3 {
        visibility: hidden;
    }
    </style>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <div style="background: linear-gradient(to right, #2d3a4a, #4b6b8d); padding: 25px; border-radius: 12px; margin-bottom: 20px;">
        <h1 style="color:white;text-align:center;">🧬 Advanced Diabetes Risk Dashboard</h1>
        <h4 style="color:white;text-align:center;">Biostatistical Exploration + Predictive Analytics + Explainability</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# Load and clean data
@st.cache_data
def load_data():
    df = pd.read_csv("diabetes.csv")
    features = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'Age']
    for col in features:
        df[col] = df[col].replace(0, np.nan)
        df[col] = df[col].fillna(df[col].median())
    return df, features

df, features = load_data()
X = df[features]
y = df['Outcome']

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Horizontal navigation
selected_tab = option_menu(
    menu_title=None,
    options=["🏠 Overview", "🔮 Predict", "📊 Analytics", "📥 Recommendation","🧠 Explain", "📥 Export"],
    icons=["house", "activity", "bar-chart", "brain", "cloud-download", "cloud-download"],
    orientation="horizontal",
    default_index=0
)

# Import modules dynamically
from overview import render_overview
from predict import render_predict
from analytics import render_analytics
from recommendation_page import render_recommendation_page  # ✅ not the function directly
from explain import render_explain
from export import render_export

# Page router with animation
with st.spinner("Loading..."):
    if selected_tab == "🏠 Overview":
        render_overview(df)
    elif selected_tab == "🔮 Predict":
        render_predict(df, features, model)
    elif selected_tab == "📊 Analytics":
         render_analytics(df, features, model)
    elif selected_tab == "📥 Recommendation":
         render_recommendation_page()
    elif selected_tab == "🧠 Explain":
        render_explain(df, features, model)
    elif selected_tab == "📥 Export":
        render_export(df, features)
