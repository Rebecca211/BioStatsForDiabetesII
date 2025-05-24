
import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression

# Page config
st.set_page_config(
    page_title=" GlucoTrack |  DiabetesII Dashboard",
    page_icon="",
    layout="wide"
)

st.markdown(
    """
    <style>
    [data-testid="stMetric"] {
        background: linear-gradient(to right, #d9afd9, #97d9e1);
        padding: 20px;
        border-radius: 15px;
        color: #fff;
        text-align: center;
        box-shadow: 2px 2px 15px rgba(0,0,0,0.1);
    }
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 500;
    }
    .stDataFrame {
        border-radius: 10px;
        background: #ffffffcc;
        backdrop-filter: blur(6px);
        box-shadow: 0 0 10px #ccc;
    }
    .stSidebar {
        background: linear-gradient(to bottom, #f2f2f2, #d9afd9);
    }
    .block-container {
        padding: 1rem 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Load dataset
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
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Sidebar menu
st.sidebar.title("📟 Navigate")
selected_tab = st.sidebar.radio("Choose", [
    "🏠 Overview", "🔮 Predict", "📊 Analytics", "📥 Recommendation", "🧠 Explain", "📥 Export"
])

# Import pages
from overview import render_overview
from predict import render_predict
from analytics import render_analytics
from recommendation_page import render_recommendation_page
from explain import render_explain
from export import render_export

# Page switching
with st.spinner("✨ Loading the vibe..."):
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
