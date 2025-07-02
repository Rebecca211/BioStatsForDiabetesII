GlucoTrack: Diabetes Risk Prediction Web App

GlucoTrack is a Streamlit-powered web application that predicts the risk of Type II Diabetes using machine learning. Built using Python and real-world health data, the app allows users to input personal metrics and receive instant risk predictions along with recommendations and explanations.

About the Project
This capstone project was developed as part of the Master of Data Analytics program at Melbourne Institute of Technology. Our aim was to apply machine learning for preventative healthcare by building a user-friendly tool that supports early detection of diabetes.

Key Features
- Predict diabetes risk based on:
  - Glucose
  - BMI
  - Insulin
  - Age
  - Blood Pressure
  - Pregnancies
- User-friendly interface with clean UI
- Multiple ML models tested; Gradient Boosting selected
- Risk-level based recommendation system
- Explainability using SHAP plots
- Live charts and visualizations

Tech Stack
Language       : Python
Framework      : Streamlit
ML Libraries   : scikit-learn, pandas, numpy, shap
Visualization  : Plotly, Seaborn, Matplotlib
UI Styling     : Custom CSS (diabetes_theme.css)

File Structure
main.py                  ← Entry point
overview.py              ← Dashboard overview layout
predict.py               ← Risk prediction logic
recommendation.py        ← Recommendations based on risk
explain.py               ← SHAP visualizations
export.py                ← Export model results
analytics.py             ← Data analysis functions
diabetes_charts.py       ← Chart visualizations
diabetes.csv             ← Dataset (Pima Indians)
gb_model_5features.pkl   ← Trained ML model
diabetes_theme.css       ← Custom Streamlit theme
requirements.txt         ← Python dependencies
radar_profile_plot.png   ← Visual result
shap_summary_plot.png    ← SHAP interpretation
*.json                   ← Risk level recommendation templates

How to Run
1. Clone the repository:
   git clone https://github.com/Rebecca211/BioStatsForDiabetesII.git
   cd BioStatsForDiabetesII

2. Install dependencies:
   pip install -r requirements.txt

3. Launch the app:
   streamlit run main.py

Model Performance
- Best Model: Gradient Boosting Classifier
- Accuracy: ~91%
- ROC-AUC Score: ~90%
- Explanation: SHAP plots show the influence of features like Glucose, BMI, and Age.

Impact and Relevance
This project demonstrates how data science can empower preventative healthcare:
- Helps users assess diabetes risk early
- Aids clinicians with a visual, interpretable tool
- Encourages data-driven health decisions

Team Members
- Reebeka Joshi
- Anish Manandhar


Project Link
https://biostatsfordiabetesii.streamlit.app/

Contact
For suggestions or collaboration, reach out via LinkedIn: https://www.linkedin.com/in/rebekajoshi
