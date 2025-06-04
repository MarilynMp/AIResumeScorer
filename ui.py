import streamlit as st
import requests
import os

st.title("🧠 AI Resume Scorer")

# List resumes from the folder
resume_folder = "resumes"
resumes = [f for f in os.listdir(resume_folder) if f.endswith(".pdf")]

selected_resume = st.selectbox("Select a Resume", resumes)
job_description = st.text_area("Paste Job Description")

if st.button("Score Resume"):
    resume_path = os.path.join(resume_folder, selected_resume)
    response = requests.post("http://localhost:5000/score", json={
        "resume_path": resume_path,
        "job_description": job_description
    })

    if response.status_code == 200:
        st.success(response.json()["result"])
    else:
        st.error(response.json()["error"])
