import streamlit as st
import os
import base64

# כותרת יפה ומרוכזת
st.markdown(
    "<h1 style='text-align: center;'>Welcome to the GCP Refresher Course</h1>",
    unsafe_allow_html=True
)

# נתיב הקובץ PDF
PDF_PATH = "GCP_Course_final.pdf"

# בדיקת קיום הקובץ והצגה
if os.path.exists(PDF_PATH):
    with open(PDF_PATH, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        pdf_display = f"""
            <div style="display: flex; justify-content: center;">
                <iframe src="data:application/pdf;base64,{base64_pdf}" width="80%" height="800px" type="application/pdf"></iframe>
            </div>
        """
        st.markdown(pdf_display, unsafe_allow_html=True)
else:
    st.error("קובץ ה־PDF לא נמצא. ודא שהקובץ בשם GCP_Course_final.pdf נמצא בתיקייה הראשית.")
