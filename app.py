import streamlit as st
import pandas as pd
import re
import os
from PyPDF2 import PdfReader
import base64

st.set_page_config(layout="wide")

QUESTIONS_FILE = "אקסל שאלות + התשובה הנכונה.xlsx"
PDF_PATH = "GCP_Course_final.pdf"
PASSED_LOG_PATH = "output/passed_users.csv"

if not os.path.exists("output"):
    os.makedirs("output")

def display_pdf(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="700px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

st.markdown("""
    <style>
    .block-container {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
    }
    .stButton>button {
        background-color: #d8629c;
        color: white;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>יש לעבור על מצגת הקורס, בסיומה יש לענות על המבחן</h1>", unsafe_allow_html=True)

name = st.text_input("שם מלא באנגלית")
if name and not re.match(r'^[A-Za-z ]+$', name):
    st.error("יש להכניס שם באנגלית בלבד")

id_number = st.text_input("ID number")
if id_number and not re.match(r'^\d{9}$', id_number):
    st.error("מספר תעודת הזהות חייב להכיל 9 ספרות בלבד")

if st.button("אישור"):
    if name and id_number:
        st.session_state["registered"] = True
        st.session_state["name"] = name
        st.session_state["id_number"] = id_number
    else:
        st.warning("נא למלא שם ותעודת זהות")

if st.session_state.get("registered"):
    st.subheader("מצגת הקורס:")
    display_pdf(PDF_PATH)

    if st.button("עבור למבחן"):
        st.session_state["quiz_started"] = True

if st.session_state.get("quiz_started"):
    st.header("מבחן:")
    st.markdown("<p style='text-align:center;'>יש לעבור את המבחן בציון 80 לפחות על מנת להצליח</p>", unsafe_allow_html=True)

    df = pd.read_excel(QUESTIONS_FILE)

    if "questions" not in st.session_state:
        st.session_state["questions"] = df.sample(10).reset_index(drop=True)

    if "answers" not in st.session_state:
        st.session_state["answers"] = [None] * 10

    for i, row in st.session_state["questions"].iterrows():
        st.markdown(f"**{i+1}. {row['question']}**")
        options = [row["option_a"], row["option_b"], row["option_c"], row["option_d"]]
        choice = st.radio("", options, key=f"q_{i}", index=None)
        st.session_state["answers"][i] = choice

    if st.button("שלח מבחן"):
        correct = 0
        results = []

        for i, row in st.session_state["questions"].iterrows():
            selected = st.session_state["answers"][i]
            if selected == row["correct"]:
                correct += 1
            results.append({
                "question": row["question"],
                "options": [row["option_a"], row["option_b"], row["option_c"], row["option_d"]],
                "correct": row["correct"],
                "selected": selected
            })

        score = round((correct / 10) * 100, 2)
        st.write(f"ציון סופי: {correct}/10 ({score}%)")

        if score >= 80:
            st.success("כל הכבוד! עברת את המבחן, התעודה תישלח במייל")
            df_log = pd.DataFrame([[st.session_state["name"], st.session_state["id_number"]]], columns=["Name", "ID"])
            if os.path.exists(PASSED_LOG_PATH):
                df_log.to_csv(PASSED_LOG_PATH, mode="a", header=False, index=False)
            else:
                df_log.to_csv(PASSED_LOG_PATH, index=False)
        else:
            st.error("לא עברת, נסה שוב")

        st.markdown("---")
        st.subheader("פירוט התשובות:")

        for idx, result in enumerate(results):
            st.markdown(f"**{idx+1}. {result['question']}**")
            for opt in result["options"]:
                if opt == result["correct"]:
                    st.markdown(f"✅ **{opt}**")
                elif opt == result["selected"]:
                    st.markdown(f"❌ {opt}")
                else:
                    st.markdown(f"{opt}")
            st.markdown("---")
