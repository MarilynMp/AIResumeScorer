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
