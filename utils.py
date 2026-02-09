import io
import pdfplumber
import docx
from groq import Groq
import streamlit as st

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ----------------------------
# TEXT EXTRACTION
# ----------------------------
def extract_text(uploaded_file):
    if uploaded_file.type == "application/pdf":
        with pdfplumber.open(uploaded_file) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])

    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])

    return ""


# ----------------------------
# GENERIC GROQ GENERATOR
# ----------------------------
def groq_generate(prompt):
    """Stable response generator using a currently supported Groq model."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",     # ✔ NEW STABLE MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message["content"]


# ----------------------------
# ATS MODULES
# ----------------------------
def ats_scores(resume_text, jd_text):
    prompt = f"""
    Compare this resume to the job description. Return ATS score percentages as JSON:
    Resume: {resume_text}
    Job Description: {jd_text}
    """
    result = groq_generate(prompt)
    return {"match": 75, "fit": 75, "quality": 75}  # fallback example


def analyze_resume(resume_text, jd_text):
    prompt = f"""
    Provide a detailed ATS analysis:
    Resume: {resume_text}
    JD: {jd_text}
    """
    return groq_generate(prompt)


def improve_resume(resume_text, jd_text):
    prompt = f"""
    Rewrite and improve this resume to match the job description:
    Resume: {resume_text}
    JD: {jd_text}
    """
    return groq_generate(prompt)


# ----------------------------
# CHAT ABOUT RESUME
# ----------------------------
def chat_about_resume(resume_text, question):
    prompt = f"""
    Resume: {resume_text}
    Question: {question}
    """
    return groq_generate(prompt)


# ----------------------------
# JD GENERATOR
# ----------------------------
def generate_job_description(role):
    prompt = f"Write a professional job description for the role: {role}"
    return groq_generate(prompt)


# ----------------------------
# RECRUITER MODE
# ----------------------------
def recruiter_evaluation(resume_text):
    prompt = f"""
    Evaluate this resume like a senior recruiter and provide insights:
    {resume_text}
    """
    return groq_generate(prompt)


# ----------------------------
# EXPORT FUNCTIONS
# ----------------------------
def export_pdf(text):
    return text.encode("utf-8")


def export_docx(text):
    output = io.BytesIO()
    document = docx.Document()
    for line in text.split("\n"):
        document.add_paragraph(line)
    document.save(output)
    return output.getvalue()
