import streamlit as st
import pandas as pd
import random
import base64
import os

# עיצוב כללי
st.set_page_config(page_title="קורס רענון GCP", layout="wide")

st.markdown("<h1 style='text-align: center;'>יש לעבור על מצגת הקורס, ולאחר מכן לעבור למבחן</h1>", unsafe_allow_html=True)

# תצוגת PDF (במקום קישור ל-Canva)
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# הצגת הקובץ מתוך הפרויקט
pdf_path = "GCP_Course_final.pdf"
if os.path.exists(pdf_path):
    show_pdf(pdf_path)
else:
    st.error("לא נמצא קובץ המצגת GCP_Course_final.pdf בתיקיית הפרויקט")

# כל שאר הקוד שלך נשמר ללא שינוי
