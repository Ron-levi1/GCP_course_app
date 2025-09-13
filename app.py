import streamlit as st
from pathlib import Path
import base64
import pandas as pd
import os

st.set_page_config(page_title="GCP Refresher", layout="centered")

st.markdown("<h1 style='text-align: center;'>Welcome to the GCP Refresher Course</h1>", unsafe_allow_html=True)
st.markdown("### Please go over the course presentation below before taking the quiz.")

pdf_path = Path("GCP_Course_final.pdf")

if pdf_path.exists():
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.error("PDF file not found. Please make sure 'GCP_Course_final.pdf' is in the project folder.")

st.divider()

st.subheader("Quiz")
questions = {
    "1. What is the main purpose of GCP?": {
        "options": ["Ensure participant safety", "Speed up research", "Reduce costs"],
        "answer": "Ensure participant safety"
    },
    "2. Who is responsible for ensuring protocol compliance?": {
        "options": ["The Sponsor", "The CRA", "The Investigator"],
        "answer": "The Investigator"
    },
    "3. What document describes the study procedures?": {
        "options": ["CV", "Protocol", "Informed Consent Form"],
        "answer": "Protocol"
    }
}

user_answers = {}
for q, data in questions.items():
    user_answers[q] = st.radio(q, data["options"], key=q)

st.divider()

name = st.text_input("Full Name")
id_number = st.text_input("ID Number")

if st.button("Submit Quiz"):
    if not name or not id_number:
        st.warning("Please enter your name and ID number.")
    else:
        score = sum(
            user_answers[q] == data["answer"]
            for q, data in questions.items()
        )
        total = len(questions)
        passed = score >= 2

        if passed:
            st.success(f"✅ You passed the quiz! Your score: {score}/{total}")

            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            results_file = output_dir / "success_log.csv"

            if results_file.exists():
                df = pd.read_csv(results_file)
            else:
                df = pd.DataFrame(columns=["Name", "ID"])

            if not ((df["Name"] == name) & (df["ID"] == id_number)).any():
                df = pd.concat([df, pd.DataFrame([{"Name": name, "ID": id_number}])], ignore_index=True)
                df.to_csv(results_file, index=False)
        else:
            st.error(f"❌ You did not pass the quiz. Your score: {score}/{total}")
