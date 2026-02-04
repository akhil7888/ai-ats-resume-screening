import fitz
import docx
from pptx import Presentation
from sentence_transformers import SentenceTransformer
import numpy as np
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO
from docx import Document
from config import GROQ_MODEL, GROQ_API_URL
import re
from difflib import SequenceMatcher

# Load embeddings
embedder = SentenceTransformer("all-mpnet-base-v2")

# ==========================================================
# TEXT EXTRACTION
# ==========================================================
def extract_text(file):
    ext = file.name.split(".")[-1].lower()

    if ext == "pdf": return extract_pdf(file)
    if ext == "docx": return extract_docx(file)
    if ext == "pptx": return extract_pptx(file)
    return ""


def extract_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join(page.get_text() for page in doc)


def extract_docx(file):
    d = docx.Document(file)
    return "\n".join(p.text for p in d.paragraphs)


def extract_pptx(file):
    prs = Presentation(file)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)

# ==========================================================
# SKILL GAP ADVANCED LOGIC
# ==========================================================

MASTER_SKILLS = [
    "python", "machine learning", "deep learning", "nlp",
    "natural language processing", "llm", "transformers",
    "tensorflow", "pytorch", "keras", "sql", "power bi",
    "data analysis", "docker", "kubernetes", "aws", "gcp",
    "azure", "mlops", "streamlit", "faiss", "computer vision",
    "analytics", "api development", "data science"
]

SKILL_SYNONYMS = {
    "nlp": ["natural language processing"],
    "mlops": ["machine learning operations"],
    "ai": ["artificial intelligence"],
    "llm": ["large language model"]
}

def normalize(text):
    return re.sub(r"[^a-zA-Z0-9\s]", " ", text.lower())

def fuzzy_match(a, b):
    return SequenceMatcher(None, a, b).ratio() > 0.75

def extract_missing_skills(resume, jd):
    resume_text = normalize(resume)
    jd_text = normalize(jd)

    found = set()
    missing = set()

    # 1. Direct skill presence in JD
    for skill in MASTER_SKILLS:
        if skill in resume_text:
            found.add(skill)
        elif skill in jd_text:
            missing.add(skill)

    # 2. Synonym support
    for key, vals in SKILL_SYNONYMS.items():
        if key in resume_text:
            found.add(key)
        else:
            for v in vals:
                if v in jd_text:
                    missing.add(key)

    # 3. Fuzzy remove skills that already exist
    final_missing = []
    for m in missing:
        in_resume = any(fuzzy_match(m, f) for f in found)
        if not in_resume:
            final_missing.append(m)

    # 4. If nothing missing → return complete message
    if not final_missing:
        return ["No major skills missing"]

    return final_missing


def skill_gap_matrix(resume, jd):
    missing = extract_missing_skills(resume, jd)
    return [{"skill": s, "status": "Missing"} for s in missing]

# ==========================================================
# ATS & SCORES
# ==========================================================
def ats_score(resume_text, jd_text):
    v1 = embedder.encode(resume_text)
    v2 = embedder.encode(jd_text)
    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    score = int(sim * 100)
    missing = extract_missing_skills(resume_text, jd_text)
    return score, missing


def job_fit_score(resume, jd):
    v1 = embedder.encode(resume)
    v2 = embedder.encode(jd)
    sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return int(sim * 100)


def resume_quality_score(resume):
    words = len(resume.split())
    if words < 200: return 40
    if words < 400: return 60
    if words < 700: return 80
    return 95

# ==========================================================
# GROQ API CALL
# ==========================================================
def call_groq(prompt, api_key):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    body = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.25
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=60)
        data = response.json()

        if "error" in data:
            return f"❌ Groq Error: {data['error']['message']}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Network Error: {str(e)}"

# ==========================================================
# AI FEATURES
# ==========================================================
def llm_analysis(resume, jd, api_key):
    prompt = f"""
Analyze this resume vs job description.

Provide:
1. Strengths  
2. Weaknesses  
3. Missing Keywords  
4. ATS Score Improvements  
5. Rewritten bullet points  

Resume:
{resume}

Job Description:
{jd}
"""
    return call_groq(prompt, api_key)


def improve_resume(resume, jd, api_key):
    prompt = f"""
Rewrite resume in a more professional, ATS-friendly way.

Resume:
{resume}

Job Description:
{jd}
"""
    return call_groq(prompt, api_key)


def chat_with_resume(resume, question, api_key):
    prompt = f"""
Answer using ONLY this resume:

Resume:
{resume}

Question:
{question}

If missing, say "Not mentioned in resume."
"""
    return call_groq(prompt, api_key)

# ==========================================================
# EXPORT PDF (REPORTLAB UTF-8 SAFE)
# ==========================================================
def export_pdf(text):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 11)

    y = 750
    for line in text.split("\n"):
        pdf.drawString(40, y, line[:110])
        y -= 16
        if y < 40:
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = 750

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


def export_docx(text):
    doc = Document()
    for line in text.split("\n"):
        doc.add_paragraph(line)
    file_path = "improved_resume.docx"
    doc.save(file_path)
    with open(file_path, "rb") as f:
        return f.read()









# import fitz
# import docx
# from pptx import Presentation
# from sentence_transformers import SentenceTransformer
# import numpy as np
# import requests
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from io import BytesIO
# from docx import Document
# from config import GROQ_MODEL, GROQ_API_URL

# # Load embeddings
# embedder = SentenceTransformer("all-mpnet-base-v2")

# # ==========================================================
# # TEXT EXTRACTION
# # ==========================================================
# def extract_text(file):
#     ext = file.name.split(".")[-1].lower()

#     if ext == "pdf": return extract_pdf(file)
#     if ext == "docx": return extract_docx(file)
#     if ext == "pptx": return extract_pptx(file)
#     return ""


# def extract_pdf(file):
#     doc = fitz.open(stream=file.read(), filetype="pdf")
#     return " ".join(page.get_text() for page in doc)


# def extract_docx(file):
#     d = docx.Document(file)
#     return "\n".join(p.text for p in d.paragraphs)


# def extract_pptx(file):
#     prs = Presentation(file)
#     text = []
#     for slide in prs.slides:
#         for shape in slide.shapes:
#             if hasattr(shape, "text"):
#                 text.append(shape.text)
#     return "\n".join(text)

# # ==========================================================
# # ATS & SCORES
# # ==========================================================
# def ats_score(resume_text, jd_text):
#     v1 = embedder.encode(resume_text)
#     v2 = embedder.encode(jd_text)
#     sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
#     score = int(sim * 100)
#     missing = extract_missing_skills(resume_text, jd_text)
#     return score, missing


# def extract_missing_skills(resume, jd):
#     skills = [
#         "python", "machine learning", "deep learning", "nlp", "llm",
#         "rag", "sql", "docker", "kubernetes", "aws", "pytorch",
#         "tensorflow", "streamlit", "faiss", "mlops", "data science"
#     ]
#     resume_l = resume.lower()
#     jd_l = jd.lower()
#     return [s for s in skills if s in jd_l and s not in resume_l]


# def job_fit_score(resume, jd):
#     v1 = embedder.encode(resume)
#     v2 = embedder.encode(jd)
#     sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
#     return int(sim * 100)


# def resume_quality_score(resume):
#     words = len(resume.split())
#     if words < 200: return 40
#     if words < 400: return 60
#     if words < 700: return 80
#     return 95


# def skill_gap_matrix(resume, jd):
#     missing = extract_missing_skills(resume, jd)
#     return [{"skill": s, "status": "Missing"} for s in missing]

# # ==========================================================
# # GROQ API CALL
# # ==========================================================
# def call_groq(prompt, api_key):
#     headers = {
#         "Authorization": f"Bearer {api_key}",
#         "Content-Type": "application/json",
#     }

#     body = {
#         "model": GROQ_MODEL,
#         "messages": [{"role": "user", "content": prompt}],
#         "temperature": 0.25
#     }

#     try:
#         response = requests.post(GROQ_API_URL, headers=headers, json=body, timeout=60)
#         data = response.json()

#         if "error" in data:
#             return f"❌ Groq Error: {data['error']['message']}"

#         return data["choices"][0]["message"]["content"]

#     except Exception as e:
#         return f"❌ Network Error: {str(e)}"

# # ==========================================================
# # AI FEATURES
# # ==========================================================
# def llm_analysis(resume, jd, api_key):
#     prompt = f"""
# Analyze this resume vs job description.

# Provide:
# 1. Strengths
# 2. Weaknesses
# 3. Missing Keywords
# 4. ATS Score Improvements
# 5. Rewritten bullet points

# Resume:
# {resume}

# Job Description:
# {jd}
# """
#     return call_groq(prompt, api_key)


# def improve_resume(resume, jd, api_key):
#     prompt = f"""
# Rewrite resume in a more professional, ATS-friendly way.

# Resume:
# {resume}

# Job Description:
# {jd}
# """
#     return call_groq(prompt, api_key)


# def chat_with_resume(resume, question, api_key):
#     prompt = f"""
# Answer using ONLY this resume:

# Resume:
# {resume}

# Question:
# {question}

# If missing, say "Not mentioned in resume."
# """
#     return call_groq(prompt, api_key)

# # ==========================================================
# # EXPORT PDF (REPORTLAB - UTF8 SAFE)
# # ==========================================================
# def export_pdf(text):
#     buffer = BytesIO()
#     pdf = canvas.Canvas(buffer, pagesize=letter)
#     pdf.setFont("Helvetica", 11)

#     y = 750
#     for line in text.split("\n"):
#         pdf.drawString(40, y, line[:110])
#         y -= 16
#         if y < 40:
#             pdf.showPage()
#             pdf.setFont("Helvetica", 11)
#             y = 750

#     pdf.save()
#     buffer.seek(0)
#     return buffer.getvalue()


# def export_docx(text):
#     doc = Document()
#     for line in text.split("\n"):
#         doc.add_paragraph(line)
#     file_path = "improved_resume.docx"
#     doc.save(file_path)
#     with open(file_path, "rb") as f:
#         return f.read()
