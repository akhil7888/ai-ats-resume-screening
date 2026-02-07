import fitz
import docx
import json
from groq import Groq
import streamlit as st

# ---------------------------
# Load Groq Client
# ---------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------------------------
# TEXT EXTRACTION
# ---------------------------
def extract_text(file):
    """Extract text from PDF or DOCX resume."""
    if file.type == "application/pdf":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in pdf:
            text += page.get_text()
        return text

    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        document = docx.Document(file)
        return "\n".join([para.text for para in document.paragraphs])

    return ""
    

# ---------------------------
# ATS SCORE GENERATOR
# ---------------------------
def groq_generate(prompt):
    """Generic Groq response using the NEWEST AVAILABLE MODEL."""
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",   # SAFE, STABLE MODEL
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message["content"]


def ats_scores(resume, jd):
    prompt = f"""
    You are an ATS scoring AI.

    Resume:
    {resume}

    Job Description:
    {jd}

    Return ONLY valid JSON:
    {{
        "match": 0-100,
        "fit": 0-100,
        "quality": 0-100
    }}
    """

    result = groq_generate(prompt)

    try:
        data = json.loads(result)
        return data
    except:
        return {"match": 50, "fit": 50, "quality": 50}


# ---------------------------
# ATS ANALYSIS
# ---------------------------
def analyze_resume(resume, jd):
    prompt = f"""
    Provide a detailed ATS analysis for how well this resume matches the job.

    Resume:
    {resume}

    Job Description:
    {jd}

    Write in bullet points.
    """

    return groq_generate(prompt)


# ---------------------------
# IMPROVED RESUME GENERATOR
# ---------------------------
def improve_resume(resume, jd):
    prompt = f"""
    Improve this resume so it is more ATS friendly and aligned with the job description.

    Resume:
    {resume}

    Job Description:
    {jd}

    Return the improved resume text only.
    """

    return groq_generate(prompt)


# ---------------------------
# CHAT ABOUT RESUME
# ---------------------------
def chat_about_resume(resume, question):
    prompt = f"""
    You are a Resume Assistant Chatbot.

    Resume:
    {resume}

    User question:
    {question}

    Provide a helpful answer.
    """

    return groq_generate(prompt)


# ---------------------------
# JOB DESCRIPTION GENERATOR
# ---------------------------
def generate_job_description(role):
    prompt = f"""
    Generate a professional job description for the role: {role}.
    Include responsibilities, requirements, and preferred skills.
    """

    return groq_generate(prompt)


# ---------------------------
# RECRUITER MODE
# ---------------------------
def recruiter_evaluation(resume):
    prompt = f"""
    Act as a senior recruiter.
    Evaluate this resume and provide strengths, weaknesses, and hiring recommendation.

    Resume:
    {resume}
    """

    return groq_generate(prompt)


# ---------------------------
# EXPORT FUNCTIONS
# ---------------------------
def export_pdf(text):
    return text


def export_docx(text):
    return text
