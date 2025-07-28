import streamlit as st
import re
import pandas as pd
import fitz
from docx import Document
from docx2pdf import convert
import os

st.markdown(
    """
    <style>
    .block-container {
        direction: rtl;
        text-align: right;
    }
    h1, h2, h3, h4, h5, h6 {
        text-align: left;
    }
    p {
        text-align: left;
    }
    .question {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .answer {
        margin-left: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

QUESTIONS_FILE = "אקסל שאלות + התשובה הנכונה.xlsx"
CERTIFICATE_TEMPLATE = "CERTIFICATE.docx"
PRESENTATION_FILE = "assets/קורס רענון לחידוש התעודה - גרסה סופית.pdf"
OUTPUT_DIR = "output"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

st.title("welcome to the GCP refresher course")

st.header("נא להזין את פרטיך")
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
    st.markdown(
        """
        <script>
        document.documentElement.requestFullscreen();
        </script>
        """,
        unsafe_allow_html=True
    )

    if st.button("הפעל מסך מלא"):
        st.markdown(
            """
            <script>
            document.documentElement.requestFullscreen();
            </script>
            """,
            unsafe_allow_html=True
        )

    st.header("יש לעבור על מצגת הקורס, בסיומו יש לענות על המבחן")

    pdf_doc = fitz.open(PRESENTATION_FILE)
    total_slides = len(pdf_doc)

    if "slide_index" not in st.session_state:
        st.session_state["slide_index"] = 0

    page = pdf_doc[st.session_state["slide_index"]]
    pix = page.get_pixmap()
    img_path = os.path.join(OUTPUT_DIR, "temp_slide.png")
    pix.save(img_path)
    st.image(img_path, use_container_width=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("◀️ הקודם") and st.session_state["slide_index"] > 0:
            st.session_state["slide_index"] -= 1
    with col3:
        if st.button("הבא ▶️") and st.session_state["slide_index"] < total_slides - 1:
            st.session_state["slide_index"] += 1

    st.caption(f"שקופית {st.session_state['slide_index'] + 1} מתוך {total_slides}")

    if st.session_state["slide_index"] == total_slides - 1:
        if st.button("עבור למבחן"):
            st.session_state["quiz_started"] = True

if st.session_state.get("quiz_started"):
    st.header("מבחן")

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