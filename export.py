import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def render_export(df, features):
    st.subheader("Coming up next: Report & Chart Download Tools")

    st.markdown("### 📄 Download Dataset")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download Dataset as CSV", csv, "diabetes_dataset.csv", "text/csv")

    st.markdown("### 🧬 Export Risk Profile Chart")
    patient_index = st.slider("Select Patient Index for Chart Export", 0, len(df)-1, 0)
    data = df[features]
    norm = (data - data.min()) / (data.max() - data.min())
    values = norm.loc[patient_index].tolist()
    values += values[:1]

    angles = [n / float(len(features)) * 2 * np.pi for n in range(len(features))]
    angles += angles[:1]

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, linewidth=2, label=f'Patient {patient_index}')
    ax.fill(angles, values, alpha=0.3)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(features)
    ax.set_title(f"Risk Profile: Patient {patient_index}")
    ax.legend()

    buffer = BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    st.download_button("Download Radar Chart as PNG", buffer, f"patient_{patient_index}_radar.png", "image/png")
    st.success("You can now download both data and custom patient charts!")