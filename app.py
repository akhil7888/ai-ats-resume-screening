import streamlit as st
from config import APP_TITLE

from ui import (
    render_header,
    render_upload_section,
    render_ats_dashboard,
    render_jd_generator,
    render_recruiter_mode,
    render_chat_section
)

from utils import (
    extract_text,
    ats_scores,
    analyze_resume,
    improve_resume,
    chat_about_resume,
    generate_job_description,
    recruiter_evaluation,
    export_pdf,
    export_docx
)

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)

# HEADER
render_header()

# SIDEBAR NAVIGATION
menu = st.sidebar.radio(
    "Navigation",
    ["ATS Scanner", "JD Generator", "Recruiter Mode", "Chat with Resume"]
)

# -------------------------------
# ATS SCANNER
# -------------------------------
if menu == "ATS Scanner":
    resume_file, jd_text = render_upload_section()

    if st.button("🔍 Analyze Resume", use_container_width=True):
        if resume_file and jd_text:
            resume_text = extract_text(resume_file)
            st.session_state["resume_text"] = resume_text

            scores = ats_scores(resume_text, jd_text)
            analysis = analyze_resume(resume_text, jd_text)
            improved = improve_resume(resume_text, jd_text)

            render_ats_dashboard(scores, analysis, improved)

            st.download_button("⬇ Download PDF", export_pdf(improved), "improved_resume.pdf")
            st.download_button("⬇ Download DOCX", export_docx(improved), "improved_resume.docx")


# -------------------------------
# JD GENERATOR
# -------------------------------
elif menu == "JD Generator":
    role = st.text_input("Enter job role")

    if st.button("Generate JD", use_container_width=True):
        jd = generate_job_description(role)
        st.text_area("Generated JD", jd, height=300)


# -------------------------------
# RECRUITER MODE
# -------------------------------
elif menu == "Recruiter Mode":
    resume = st.session_state.get("resume_text", "")

    if resume:
        if st.button("Evaluate Resume", use_container_width=True):
            result = recruiter_evaluation(resume)
            st.write(result)
    else:
        st.warning("Upload and analyze a resume first in ATS Scanner!")


# -------------------------------
# CHAT WITH RESUME
# -------------------------------
elif menu == "Chat with Resume":
    resume = st.session_state.get("resume_text", "")
    question = render_chat_section()

    if question:
        if resume:
            answer = chat_about_resume(resume, question)
            st.write(answer)
        else:
            st.warning("Please analyze a resume in ATS Scanner first!")
