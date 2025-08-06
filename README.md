## GCP Certificate Renewal Course App

This is a Streamlit web application designed to deliver a GCP refresher course in Hebrew.  
The app includes an embedded course presentation, a randomized quiz, and generates a personalized certificate (in DOCX format) for participants who pass the exam.

## Features

- Course presentation in Hebrew
- Quiz with 10 random questions selected from a question bank
- Final score calculated and displayed to the participant
- Personalized certificate including participant's full name and ID
- Certificate saved locally in the output folder

## Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the App

Run the following command in your terminal:

```bash
streamlit run gcp_cert_app.py
```

This will open the app in your default browser at:

```
http://localhost:8501
```

## Files in the Repository

- `gcp_cert_app.py` – Main application code  
- `CERTIFICATE.docx` – Template for personalized certificates  
- `requirements.txt` – List of required Python libraries  
- `README.md` – Description and usage instructions  
- `.gitignore` – Files and folders excluded from version control  
- `אקסל שאלות + התשובה הנכונה.xlsx` – Quiz question bank  
- `output/` – Folder where generated certificates are saved  

## Access

This app is private and only accessible to users with the Streamlit sharing link.  
Participants must pass the quiz with a minimum score of 80 to receive a certificate.

## Created by

Ron Levi
