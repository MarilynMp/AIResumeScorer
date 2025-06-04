Steps
1) Downloaded and installed Python : 3.13.3 from https://www.python.org/downloads/
(Make note of the path where it is being installed during installation : Mine for eg was C:\Users\{UserName}\AppData\Local\Programs\Python\Python313)
2) In System Env Variables -> Path, added 
C:\Users\{UserName}\AppData\Local\Programs\Python\Python313
C:\Users\{UserName}\AppData\Local\Programs\Python\Python313\Scripts

3) Go to your project folder
And run : 
3a) python -m venv openai-env
3b) openai-env\Scripts\activate --> run this in cmd
3c) pip install openai

4) Create an .env file in the same project folder and add below content
OPENAI_API_KEY=your_api_key_here

5) Project structure
resume-scorer/
├── resumes/                  # Folder where your resumes are stored
│   └── sample_resume.pdf
├── app.py                    # Flask backend API
├── scorer.py                 # Core logic to score resume using OpenAI
├── ui.py                     # Streamlit frontend
├── .env                      # API key stored here
├── requirements.txt
└── .gitignore

6) My Prompt :
I have to build a AI resume scorer app. UI I was thinking streamlit to keep it easy, Backend flask api and open ai to calculate score. I will to start with store my resume's in a folder , the input to endpont will be resume path and job description and output will be resume match score using open ai. The api key is present in env variable named OPENAI_API_KEY.
Can you give me the code for all this in a structured manner ?

Response :
✅ 1. .env (Environment Variable File)
ini
Copy
Edit
OPENAI_API_KEY=your-api-key-here
✅ 2. requirements.txt
txt
Copy
Edit
flask
python-dotenv
openai
PyPDF2
streamlit
Install everything with:

bash
Copy
Edit
pip install -r requirements.txt
✅ 3. scorer.py (OpenAI Score Logic)
python
Copy
Edit
import os
import openai
from dotenv import load_dotenv
import PyPDF2

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def score_resume(resume_path, job_description):
    resume_text = extract_text_from_pdf(resume_path)

    prompt = f"""
You are an AI assistant that matches resumes to job descriptions.
Given the following resume and job description, provide a match score between 0 and 100 with a short reason.

Resume:
{resume_text}

Job Description:
{job_description}

Respond in this format:
Score: <score>/100
Reason: <reason>
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']
✅ 4. app.py (Flask Backend)
python
Copy
Edit
from flask import Flask, request, jsonify
from scorer import score_resume
import os

app = Flask(__name__)

@app.route("/score", methods=["POST"])
def score():
    data = request.json
    resume_path = data.get("resume_path")
    job_description = data.get("job_description")

    if not resume_path or not job_description:
        return jsonify({"error": "Missing resume_path or job_description"}), 400

    if not os.path.exists(resume_path):
        return jsonify({"error": "Resume file not found"}), 404

    result = score_resume(resume_path, job_description)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
✅ 5. ui.py (Streamlit Frontend)
python
Copy
Edit
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
✅ 6. How to Run It All
Start Flask API:
bash
Copy
Edit
python app.py
In a new terminal, run Streamlit UI:
bash
Copy
Edit
streamlit run ui.py

7) My Prompt how to debug?
✅ Using VS Code for GUI Debugging (Recommended)
1. Open your project folder in VS Code.
2. Create a file .vscode/launch.json:
json
Copy
Edit
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask: Debug",
      "type": "python",
      "request": "launch",
      "module": "flask",
      "env": {
        "FLASK_APP": "app.py",
        "FLASK_ENV": "development"
      },
      "args": ["run"],
      "jinja": true
    }
  ]
}

3. Press F5 or click the green ▶️ "Run" button.
You can now:

Set breakpoints (just click next to line numbers)

Step through code

Inspect variables in the debugger panel


