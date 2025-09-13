import streamlit as st
import base64
import pandas as pd
import random
import os

# הגדרת הקובץ
PDF_PATH = "GCP_Course_final.pdf"

# הצגת כותרת
st.markdown("<h2 style='text-align: center;'>יש לעבור על מצגת הקורס, ולאחר מכן לעבור למבחן</h2>", unsafe_allow_html=True)

# פונקציה להצגת PDF
def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode("utf-8")
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800px" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# הצגת הקובץ
if os.path.exists(PDF_PATH):
    show_pdf(PDF_PATH)
else:
    st.error(f"לא נמצא קובץ PDF בשם: {PDF_PATH}")

# קו הפרדה
st.markdown("---")
st.markdown("### לאחר שסיימת לעיין במצגת – תוכל לגשת למבחן:")
