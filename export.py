import streamlit as st
import pandas as pd
import base64
from io import BytesIO
from fpdf import FPDF
from datetime import datetime
import qrcode


def render_export(df, features):
    st.markdown("## 📥 Export Patient Report")
    st.markdown("Download a PDF summary of prediction results, charts, and recommendations.")

    # Custom styling for sidebar navigation (bigger font and padding)
    st.markdown("""
    <style>
    [data-testid="stSidebar"] .css-1v0mbdj, [data-testid="stSidebar"] .css-1d391kg {
        font-size: 1.1rem !important;
        font-weight: 600;
        padding: 1rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'user_input' not in st.session_state or 'user_prediction' not in st.session_state:
        st.warning("⚠️ Please run a prediction first on the Predict tab.")
        return

    user_input = st.session_state['user_input']
    prediction = st.session_state['user_prediction']

    # Ask for patient identity
    st.subheader("👤 Patient Identification")
    patient_name = st.text_input("Full Name", "")
    patient_id = st.text_input("Patient ID or Reference", "")

    st.subheader("📝 Patient Details")
    st.json(user_input)

    st.subheader("🧠 Prediction")
    st.write("**Outcome:**", "🩺 Diabetes" if prediction['class'] else "✅ No Diabetes")
    st.write("**Confidence:**", f"{prediction['prob']*100:.2f}%")

    st.subheader("💡 Recommendation")
    if prediction['class']:
        st.error("Patient is likely diabetic. Please consult a healthcare provider.")
    else:
        st.success("No diabetes detected. Encourage healthy lifestyle practices.")

    if st.button("📄 Generate PDF Report"):
        with st.spinner("Generating report..."):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_fill_color(0, 85, 140)
            pdf.set_text_color(255, 255, 255)
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 12, txt="Bangladesh Medical Society of Victoria", ln=1, align='C', fill=True)

            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", size=12)
            pdf.ln(5)
            pdf.cell(200, 10, txt="Diabetes Risk Report", ln=1, align='C')
            pdf.ln(5)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            pdf.set_font("Arial", size=10)
            pdf.cell(200, 8, txt=f"Report Generated: {timestamp}", ln=1, align='R')

            if patient_name or patient_id:
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(200, 10, txt="Patient Identification:", ln=1)
                pdf.set_font("Arial", size=11)
                if patient_name:
                    pdf.cell(200, 8, txt=f"Name: {patient_name}", ln=1)
                if patient_id:
                    pdf.cell(200, 8, txt=f"ID: {patient_id}", ln=1)
                pdf.ln(5)

            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, txt="Patient Details:", ln=1)
            pdf.set_font("Arial", size=10)
         
            details = list(user_input.items())
            for i in range(0, len(details), 3):
                row = details[i:i+3]
                for k, v in row:
                    pdf.cell(63, 8, txt=f"{k}: {v}", border=0)
                pdf.ln(8)


            pdf.ln(5)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, txt="Prediction:", ln=1)
            pdf.set_font("Arial", size=11)
            outcome = "Diabetes" if prediction['class'] else "No Diabetes"
            pdf.cell(200, 8, txt=f"Outcome: {outcome}", ln=1)
            pdf.cell(200, 8, txt=f"Confidence: {prediction['prob']*100:.2f}%", ln=1)

            pdf.ln(5)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, txt="Recommendation:", ln=1)
            pdf.set_font("Arial", size=10)
            if prediction['class']:
                pdf.multi_cell(0, 8, "High risk of diabetes detected. Recommend clinical testing, healthy diet, and exercise.")
            else:
                pdf.multi_cell(0, 8, "No diabetes risk detected. Maintain a healthy lifestyle and monitor regularly.")

            pdf.ln(5)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, txt="Doctor's Notes:", ln=1)
            pdf.set_font("Arial", size=11)
            pdf.multi_cell(0, 8, "......................................................................................................\n\n...........................................................................")

            # --- Analytics Visuals ---
            pdf.ln(5)
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(200, 10, txt="Analytics Visuals:", ln=1)

            if "shap_path" in st.session_state and "radar_path" in st.session_state:
                # Two charts side by side on the same row using manual positions
                pdf.image(st.session_state["shap_path"], x=10, y=pdf.get_y(), w=95)
                pdf.image(st.session_state["radar_path"], x=105, y=pdf.get_y(), w=95)
                pdf.ln(70)  # Adjust based on image height
            else:
                pdf.set_font("Arial", 'I', 11)
                pdf.cell(200, 10, txt="(Charts not available. Please visit Analytics tab first.)", ln=1)

            pdf.ln(10)
            pdf.set_text_color(0, 85, 140)
            pdf.set_font("Arial", 'I', 8)
            pdf.cell(200, 10, txt="© Bangladesh Medical Society of Victoria | https://bmsvictoria.org.au", ln=1, align='C')

            pdf_bytes = pdf.output(dest='S').encode('latin1')

            st.download_button(
                label="📄 Download PDF",
                data=pdf_bytes,
                file_name="diabetes_report_bmsv.pdf",
                mime="application/pdf"
            )
