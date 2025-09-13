import streamlit as st
import pandas as pd
import random
import os
from docx import Document
from docx.shared import Pt
from docx2pdf import convert

st.set_page_config(page_title="קורס רענון GCP", layout="wide")

st.markdown("<h1 style='text-align: center;'>קורס רענון GCP</h1>", unsafe_allow_html=True)

pdf_path = "GCP_Course_final.pdf"

if os.path.exists(pdf_path):
    with open(pdf_path, "rb") as f:
        base64_pdf = f.read().encode("base64")
    st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>', unsafe_allow_html=True)
else:
    st.error("קובץ PDF לא נמצא. ודא שהוא קיים בתיקייה הראשית בשם GCP_Course_final.pdf")

st.markdown("---")

st.header("הזדהות לפני תחילת המבחן")
name = st.text_input("שם מלא")
id_number = st.text_input("תעודת זהות")

if name and id_number:
    st.success("ברוך הבא, " + name)
    st.markdown("---")

    # שאלות
    st.subheader("שאלון")
    df = pd.read_excel("אקסל שאלות + תשובות הנכונה.xlsx")
    questions = df.sample(10).reset_index(drop=True)
    user_answers = []

    for i, row in questions.iterrows():
        q = row["שאלה"]
        options = [row["תשובה 1"], row["תשובה 2"], row["תשובה 3"], row["תשובה 4"]]
        user_choice = st.radio(f"שאלה {i+1}: {q}", options, key=i)
        user_answers.append(user_choice)

    if st.button("סיים ושלח"):
        correct = 0
        results = []

        for i, row in questions.iterrows():
            correct_answer = row["תשובה נכונה"]
            explanation = row["הסבר"]
            is_correct = user_answers[i] == correct_answer
            if is_correct:
                correct += 1
            results.append((row["שאלה"], user_answers[i], correct_answer, explanation, is_correct))

        st.markdown("---")
        st.subheader("תוצאות")

        st.write(f"ענית נכון על {correct} מתוך 10")

        for i, (q, ans, corr, expl, correct_flag) in enumerate(results):
            st.markdown(f"**שאלה {i+1}:** {q}")
            st.markdown(f"- התשובה שלך: {ans}")
            st.markdown(f"- התשובה הנכונה: {corr}")
            st.markdown(f"- הסבר: {expl}")
            st.markdown("---")

        if correct >= 8:
            st.success("עברת את המבחן בהצלחה! ניצור עבורך תעודה 🎓")

            doc = Document()
            style = doc.styles['Normal']
            font = style.font
            font.name = 'Arial'
            font.size = Pt(14)

            doc.add_heading('תעודת סיום קורס רענון GCP', 0)
            doc.add_paragraph(f'זוהי תעודה המעידה כי {name}, ת.ז. {id_number}, עבר/ה בהצלחה את מבחן הרענון של קורס GCP.')
            doc.add_paragraph(f'הציון הסופי: {correct} מתוך 10.')
            doc.add_paragraph('בברכה,\nרשות המחקר – המרכז הרפואי שיבא תל השומר')

            word_path = f'output/certificate_{id_number}.docx'
            pdf_path = f'output/certificate_{id_number}.pdf'

            os.makedirs("output", exist_ok=True)
            doc.save(word_path)
            convert(word_path, pdf_path)

            with open(pdf_path, "rb") as pdf_file:
                btn = st.download_button(
                    label="הורד תעודה כקובץ PDF",
                    data=pdf_file,
                    file_name=f"certificate_{id_number}.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("לצערנו לא עברת את המבחן. תוכל לנסות שוב.")
