import streamlit as st
import re
import pandas as pd
import os
import base64

# הגדרות עיצוב
st.markdown("""
    <style>
    .block-container { direction: rtl; text-align: right; font-family: Arial, sans-serif; }
    h1, h2, h3, h4, h5, h6 { text-align: center; font-family: Arial, sans-serif; }
    p, label, .stRadio, .stButton { font-family: Arial, sans-serif; }
    .stButton>button {
        background-color: #d8629c;
        color: white;
        padding: 10px 24px;
        text-align: center;
        font-size: 16px;
        margin: 4px 2px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #d8629c;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# פונקציה להצגת PDF מקומי
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="750" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


QUESTIONS_FILE = "אקסל שאלות + התשובה הנכונה.xlsx"

# כותרת
st.markdown("""
    <div style='display: flex; justify-content: center; align-items: center;'>
        <h1 style='color: #d89bb9; font-family: Arial, sans-serif; font-size: 50px; font-weight: bold;
         text-shadow: 2px 2px 4px #aaa; margin: 20px 0; white-space: nowrap;'>
        Welcome to the GCP Refresher Course</h1>
    </div>
""", unsafe_allow_html=True)

# טופס התחברות
st.markdown("<h2 style='text-align:right; direction:rtl;'>יש להזין את פרטיך</h2>", unsafe_allow_html=True)
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

# אחרי התחברות
if st.session_state.get("registered"):
    st.markdown("<h2 style='text-align:center; direction:rtl;'>יש לעבור על מצגת הקורס, בסיומה יש לענות על המבחן</h2>",
                unsafe_allow_html=True)
    st.markdown(
        "<h2 style='text-align:center; direction:rtl;font-size: 16px;'>לנוחיותכם, יש להגדיל את המצגת למסך מלא</h2>",
        unsafe_allow_html=True)

    show_pdf("GCP_Course_final.pdf")  # הצגת קובץ ה־PDF המקומי

    if st.button("עבור למבחן"):
        st.session_state["quiz_started"] = True

# מבחן
if st.session_state.get("quiz_started"):
    st.markdown("<h2 style='text-align:center; direction:rtl;'>מבחן:</h2>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align:center; direction:rtl; color:gray; font-size:17px; font-weight:normal;margin-bottom:30px;'>יש לעבור את המבחן בציון 80 לפחות על מנת לקבל את התעודה</h3>",
        unsafe_allow_html=True)

    df = pd.read_excel(QUESTIONS_FILE)

    if "questions" not in st.session_state:
        st.session_state["questions"] = df.sample(10).reset_index(drop=True)

    questions = st.session_state["questions"]

    if "answers" not in st.session_state:
        st.session_state["answers"] = [None] * len(questions)

    for i, row in questions.iterrows():
        st.markdown(f"<div class='question'>{i + 1}. {row['question']}</div>", unsafe_allow_html=True)
        selected = st.radio(
            "",
            [row['option_a'], row['option_b'], row['option_c'], row['option_d']],
            index=None,
            key=f"q_{i}"
        )
        st.session_state["answers"][i] = selected if selected else st.session_state["answers"][i]
        st.markdown("<br>", unsafe_allow_html=True)

    if st.button("שלח מבחן"):
        correct = 0
        results = []

        for i, row in questions.iterrows():
            user_answer = st.session_state["answers"][i]
            if user_answer == row['correct']:
                correct += 1
            results.append({
                "question": row['question'],
                "options": [row['option_a'], row['option_b'], row['option_c'], row['option_d']],
                "correct": row['correct'],
                "selected": user_answer
            })

        score = round((correct / 10) * 100, 2)
        st.write(f"ציון סופי: {correct}/10 ({score}%)")

        if score >= 80:
            st.success("כל הכבוד! עברת את הרענון בהצלחה.")
        else:
            st.error("לא עברת את המבחן. נסה שוב.")

        # פירוט תשובות – תמיד מוצג
        st.markdown("---")
        st.subheader("פירוט התשובות")
        for idx, result in enumerate(results):
            st.markdown(f"**{idx + 1}. {result['question']}**")
            for opt in result["options"]:
                if opt == result["correct"]:
                    st.markdown(f"✅ **{opt}**")
                elif opt == result["selected"]:
                    st.markdown(f"❌ {opt}")
                else:
                    st.markdown(f"{opt}")
            st.markdown("---")
