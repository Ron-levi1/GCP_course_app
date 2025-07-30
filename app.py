import streamlit as st
import re
import pandas as pd
from docx import Document
from docx2pdf import convert
import os

st.markdown(
    """
    <style>
    .block-container {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
        font-family: Arial, sans-serif;
    }
    p, label, .stRadio, .stButton {
        font-family: Arial, sans-serif;
    }
    .stButton>button {
        background-color: #d8629c;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        transition-duration: 0.4s;
        border: none;
    }
    .stButton>button:hover {
        background-color: #d8629c;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    .block-container {
        direction: rtl;
        text-align: right;
        font-family: Arial, sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p {
        font-family: Arial, sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .block-container {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: center;
    }
    p {
        text-align: right;
    }
    .question {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .answer {
        margin-left: 20px;
    }
    iframe {
        border: none;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

QUESTIONS_FILE = "אקסל שאלות + התשובה הנכונה.xlsx"
CERTIFICATE_TEMPLATE = "CERTIFICATE.docx"
OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

import streamlit as st

st.markdown(
    """
    <h1 style='text-align: center; 
               color: #4CAF50; 
               font-family: Arial, sans-serif; 
               font-size: 50px;
               text-shadow: 2px 2px 4px #aaa;'>
        Welcome to the GCP Refresher Course
    </h1>
    """, unsafe_allow_html=True
)

st.markdown("<h2 style='text-align:right; direction:rtl;'>נא להזין את פרטיך</h2>", unsafe_allow_html=True)

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

    st.markdown("<h2 style='text-align:center; direction:rtl;'>יש לעבור על מצגת הקורס, בסיומה יש לענות על המבחן</h2>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; direction:rtl;font-size: 16px;'>לנוחיותכם, יש להגדיל את המצגת למסך מלא</h2>",
                unsafe_allow_html=True)

    st.markdown(
        """
        <div style="position: relative; width: 100%; height: 0; padding-top: 56.2500%;
 padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden;
 border-radius: 8px; will-change: transform;">
  <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
    src="https://www.canva.com/design/DAGksdqsOYk/WuwpZFV-DcQPubRJQp4rBA/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
  </iframe>
</div>
<a href="https:&#x2F;&#x2F;www.canva.com&#x2F;design&#x2F;DAGksdqsOYk&#x2F;WuwpZFV-DcQPubRJQp4rBA&#x2F;view?utm_content=DAGksdqsOYk&amp;utm_campaign=designshare&amp;utm_medium=embeds&amp;utm_source=link" target="_blank" rel="noopener">קורס רענון לחידוש התעודה - גרסה סופית</a> by Ron Levi
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        a[href*="canva.com"] {
            display: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("עבור למבחן"):
        st.session_state["quiz_started"] = True

if st.session_state.get("quiz_started"):
    st.markdown("<h2 style='text-align:center; direction:rtl;'>מבחן:</h2>",
                unsafe_allow_html=True)

    st.markdown(
        "<h3 style='text-align:center; direction:rtl; color:gray; font-size:17px; font-weight:normal;margin-bottom:30px;'>יש לעבור את המבחן בציון 80 לפחות על מנת לקבל את התעודה</h3>",
        unsafe_allow_html=True)

    df = pd.read_excel(QUESTIONS_FILE)
    questions = df.sample(15).reset_index(drop=True)

    answers = []
    for i, row in questions.iterrows():
        st.markdown(f"<div class='question'>{i+1}. {row['question']}</div>", unsafe_allow_html=True)
        ans = st.radio(
            "",
            [row['option_a'], row['option_b'], row['option_c'], row['option_d']],
            key=f"q_{i}"
        )
        answers.append(ans)
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("שלח מבחן"):
        correct = 0
        for i, row in questions.iterrows():
            if answers[i] == row['correct']:
                correct += 1

        score = (correct / 15) * 100
        st.write(f"ציון סופי: {correct}/15 ({score}%)")

        if score >= 80:
            st.success("עברת את המבחן")

            cert_doc = Document(CERTIFICATE_TEMPLATE)
            for p in cert_doc.paragraphs:
                if "[the name]" in p.text:
                    p.text = p.text.replace("[the name]", st.session_state["name"])
                if "[the ID]" in p.text:
                    p.text = p.text.replace("[the ID]", st.session_state["id_number"])

            filled_docx = os.path.join(OUTPUT_DIR, "תעודה_אישית.docx")
            cert_doc.save(filled_docx)

            filled_pdf = os.path.join(OUTPUT_DIR, "תעודה_אישית.pdf")
            convert(filled_docx, filled_pdf)

            with open(filled_pdf, "rb") as f:
                file_name = f"GCP Certificate - {st.session_state['name']}.pdf"
                st.download_button("הורד תעודה", f, file_name=file_name)
        else:
            st.error("לא עברת את המבחן. נסה שוב.")
