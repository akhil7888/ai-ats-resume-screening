import streamlit as st
from config import APP_TITLE

# Import matching UI functions
from ui import (
    render_header,
    render_upload_section,
    render_ats_dashboard,
    render_skill_gaps,
    render_jd_generator,
    render_recruiter_mode,
    render_chat_section
)

# Import utilities
from utils import (
    extract_text,
    ats_scores,
    analyze_resume,
    improve_resume,
    export_pdf,
    export_docx
)

# Page settings
st.set_page_config(page_title=APP_TITLE, layout="wide")

# Load Styles
st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)

# Sidebar Navigation
menu = st.sidebar.radio(
    "Navigation",
    ["ATS Scanner", "JD Generator", "Recruiter Mode", "Chat with Resume"]
)

# Header
render_header()

# ROUTER
if menu == "ATS Scanner":
    resume_file, jd_text = render_upload_section()

    if st.button("🔍 Analyze Resume", use_container_width=True):
        if resume_file and jd_text:
            with st.spinner("Analyzing with Groq AI…"):
                resume_text = extract_text(resume_file)
                scores = ats_scores(resume_text, jd_text)
                analysis = analyze_resume(resume_text, jd_text)
                improved = improve_resume(resume_text, jd_text)

            # Show ATS Results
            render_ats_dashboard(scores, analysis, improved)

            # Download Buttons
            st.download_button("⬇ Download PDF", export_pdf(improved), "improved_resume.pdf")
            st.download_button("⬇ Download DOCX", export_docx(improved), "improved_resume.docx")

elif menu == "JD Generator":
    render_jd_generator()

elif menu == "Recruiter Mode":
    render_recruiter_mode()

elif menu == "Chat with Resume":
    render_chat_section()
