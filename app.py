import streamlit as st
import pandas as pd
import random
import base64

# כותרת
st.markdown("<h2 style='text-align: center;'>יש לעבור על מצגת הקורס, בסיומה יש לענות על המבחן</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: small;'>לתשומת לבכם, יש להגדיל את המצגת לתצוגה מלאה</p>", unsafe_allow_html=True)

# הצגת קובץ PDF של הקורס
with open("GCP_Course_final.pdf", "rb") as f:
    base64_pdf = base64.b64encode(f.read()).decode("utf-8")
pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="600px" type="application/pdf"></iframe>'
st.markdown(pdf_display, unsafe_allow_html=True)

# מעבר למבחן
if st.button("עבור למבחן"):
    st.session_state.quiz_started = True

# אם המשתמש עבר למבחן
if st.session_state.get("quiz_started", False):
    st.markdown("### מבחן רענון GCP")

    # טעינת קובץ השאלות
    df = pd.read_excel("gcp_questions.xlsx")

    # בחירת 10 שאלות אקראיות
    sample_questions = df.sample(n=10).reset_index(drop=True)

    # הצגת שאלות ואיסוף תשובות
    user_answers = []
    for i, row in sample_questions.iterrows():
        st.write(f"**שאלה {i+1}:** {row['שאלה']}")
        options = [row['תשובה 1'], row['תשובה 2'], row['תשובה 3'], row['תשובה 4']]
        user_choice = st.radio("", options, key=f"q_{i}")
        user_answers.append(user_choice)
        st.markdown("---")

    if st.button("סיים מבחן"):
        score = 0
        results = []

        for i, row in sample_questions.iterrows():
            correct_answer = row['תשובה נכונה']
            explanation = row['הסבר']
            user_choice = user_answers[i]
            is_correct = user_choice == correct_answer
            if is_correct:
                score += 1
            results.append({
                "שאלה": row['שאלה'],
                "תשובתך": user_choice,
                "תשובה נכונה": correct_answer,
                "האם ענית נכון?": "✔️" if is_correct else "❌",
                "הסבר": explanation
            })

        # הצגת תוצאה
        st.markdown(f"## ✅ קיבלת {score} מתוך 10")

        # הצגת טבלת הסברים מלאה
        results_df = pd.DataFrame(results)
        st.markdown("### הסברים לכל שאלה:")
        st.dataframe(results_df)

