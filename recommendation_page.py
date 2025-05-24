import streamlit as st
from recommendation import render_recommendation

def render_recommendation_page():
    st.subheader("📥 Personalized Health Recommendations")

    if 'user_prediction' not in st.session_state:
        st.info("👈 Please predict first using the Predict tab.")
        return

    user_prob = st.session_state['user_prediction']['prob']
    render_recommendation(user_prob)
