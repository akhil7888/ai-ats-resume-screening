import streamlit as st
from config import APP_TITLE
from ui import (
    render_header,
    render_upload_section,
    render_ats_dashboard,
    render_jd_generator_section,
    render_recruiter_section,
    render_chat_section
)
from utils import (
    extract_text,
    ats_scores,
    analyze_resume,
    improve_resume,
    generate_job_description,
    recruiter_evaluation,
    chat_about_resume
)

st.set_page_config(page_title=APP_TITLE, layout="wide")

render_header()

menu = st.sidebar.radio("Navigation", [
    "ATS Scanner", "JD Generator", "Recruiter Mode", "Chat with Resume"
])

if menu == "ATS Scanner":
    resume_file, jd_text = render_upload_section()

    if st.button("🔍 Analyze Resume"):
        if resume_file and jd_text:
            resume_text = extract_text(resume_file)

            st.session_state["resume_text"] = resume_text

            scores = ats_scores(resume_text, jd_text)
            analysis = analyze_resume(resume_text, jd_text)
            improved = improve_resume(resume_text, jd_text)

            render_ats_dashboard(scores, analysis, improved)

elif menu == "JD Generator":
    role = render_jd_generator_section()
    if st.button("Generate JD"):
        jd = generate_job_description(role)
        st.text_area("Generated JD", jd, height=300)

elif menu == "Recruiter Mode":
    resume = st.session_state.get("resume_text", "")
    if resume and render_recruiter_section(resume):
        st.write(recruiter_evaluation(resume))

elif menu == "Chat with Resume":
    resume = st.session_state.get("resume_text", "")
    question = render_chat_section(resume)
    if question:
        st.write(chat_about_resume(resume, question))
