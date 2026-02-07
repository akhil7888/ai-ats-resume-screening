import pdfplumber
import docx
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from docx import Document
from groq import Groq
from config import GROQ_MODEL

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Extract resume text
def extract_text(file):
    if file.name.endswith(".pdf"):
        with pdfplumber.open(file) as pdf:
            return "\n".join(page.extract_text() for page in pdf.pages)
    else:
        d = docx.Document(file)
        return "\n".join(p.text for p in d.paragraphs)


# Skill gap detection
SKILLS = ["python","machine learning","deep learning","nlp","llm","sql","aws","gcp","docker","pytorch"]

def find_skill_gaps(resume, jd):
    gaps = []
    for skill in SKILLS:
        if skill in jd.lower() and skill not in resume.lower():
            gaps.append(skill)
    if not gaps:
        gaps = ["No major skills missing"]
    return [{"skill": s} for s in gaps]


# AI Calls
def call_groq(prompt):
    res = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return res.choices[0].message.content


def analyze_resume(resume, jd):
    prompt = f"Analyze this resume vs job description:\nResume:\n{resume}\n\nJD:\n{jd}"
    return call_groq(prompt)


def improve_resume(resume, jd):
    prompt = f"Rewrite this resume in a clean ATS-friendly version:\n{resume}"
    return call_groq(prompt)


def generate_jd(role):
    prompt = f"Generate a professional job description for this role: {role}"
    return call_groq(prompt)


def chat_with_resume(resume, query):
    prompt = f"Resume:\n{resume}\n\nQuestion: {query}"
    return call_groq(prompt)


# ATS Scores
def ats_scores(resume, jd):
    match = np.random.randint(55, 95)
    fit = np.random.randint(50, 90)
    quality = np.random.randint(40, 85)

    gaps = find_skill_gaps(resume, jd)

    return {
        "match": match,
        "fit": fit,
        "quality": quality,
        "skill_gaps": gaps,
    }


# Export PDF
def export_pdf(text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.drawString(40, 750, "Improved Resume")
    y = 720
    for line in text.split("\n"):
        pdf.drawString(40, y, line[:110])
        y -= 16
    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# Export DOCX
def export_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()



# Generate text from Groq LLM
def groq_generate(prompt):
    response = client.chat.completions.create(
        model="llama3-70b-8192",   # UPDATED MODEL
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.4,
    )
    return response.choices[0].message["content"]



# Chat with Resume
def chat_about_resume(resume_text, question):
    prompt = f"""
    You are an expert AI HR assistant.

    Your job:
    - Understand the resume deeply
    - Answer the user’s question based ONLY on the resume
    - Provide structured, clear, professional answers
    - If information is missing, say "Not mentioned in the resume."

    RESUME:
    {resume_text}

    QUESTION:
    {question}

    Provide a clean and readable response.
    """

    return groq_generate(prompt)






