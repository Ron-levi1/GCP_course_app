import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import os

# הגדרות קובץ המצגת
PDF_PATH = "GCP_Course_final.pdf"
OUTPUT_DIR = "output"
LOG_PATH = os.path.join(OUTPUT_DIR, "success_log.csv")

# ודא שתיקיית פלט קיימת
os.makedirs(OUTPUT_DIR, exist_ok=True)

# עיצוב דחוס יותר
st.markdown("""
    <style>
    .main { max-width: 1000px; margin: auto; }
    .title { text-align: center; font-size: 36px; font-weight: bold; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# כותרת בעיצוב מותאם
st.markdown('<div class="title">Welcome to the GCP Refresher Course</div>', unsafe_allow_html=True)

# הוראות כלליות
st.markdown("### 🧠 כדי לעבור על הקורס, יש לצפות במצגת המלאה ולאחר מכן לעבור למבחן")

# מציג את המצגת (PDF)
try:
    with open(PDF_PATH, "rb") as f:
        reader = PdfReader(f)
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                st.markdown(f"#### Slide {i + 1}")
                st.write(text)
except FileNotFoundError:
    st.error("הקובץ GCP_Course_final.pdf לא נמצא. ודא שהוא בתיקיית הפרויקט!")

# קבלת שם ומספר תעודת זהות מהמשתמש
st.markdown("### 📋 אנא הזינו את פרטיכם כדי להיבחן")
name = st.text_input("שם מלא")
id_number = st.text_input("מספר תעודת זהות")

# כפתור התחלת מבחן (כרגע רק שומר את הפרטים בקובץ CSV)
if st.button("אני מוכן/ה למבחן"):
    if name and id_number:
        df = pd.DataFrame([[name, id_number]], columns=["Name", "ID"])
        if os.path.exists(LOG_PATH):
            df.to_csv(LOG_PATH, mode='a', header=False, index=False)
        else:
            df.to_csv(LOG_PATH, index=False)
        st.success("נרשמת בהצלחה! בהצלחה במבחן 🎓")
    else:
        st.warning("נא למלא את כל השדות")
