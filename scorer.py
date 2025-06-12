import os
import json
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2

load_dotenv()

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def score_resume(resume_path, job_description):
    resume_text = extract_text_from_pdf(resume_path)

    prompt = f"""
    You are a job matching assistant. Evaluate the resume and job description below.

    1. Give a **score between 0 and 100**
    2. Give a **brief reason for the score**
    3. List **matching skills**
    4. List **missing skills** that the job description requires but are not in the resume.

    Use the following JSON format:

    {{
        "score": <score>,
        "reason": "<reason>",
        "matching_skills": ["skill1", "skill2", ...],
        "missing_skills": ["skillA", "skillB", ...]
    }}

    Resume:
    \"\"\"
    {resume_text}
    \"\"\"

    Job Description:
    \"\"\"
    {job_description}
    \"\"\"
    """

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)



