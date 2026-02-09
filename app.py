import streamlit as st
from config import APP_TITLE
from ui import (
    render_header,
    render_upload_section,
    render_ats_dashboard,
    render_chat_section
)
from utils import (
    extract_resume_text,
    ats_scores,
    analyze_resume,
    improve_resume,
    chat_about_resume
)
from recruiter import recruiter_evaluation

st.set_page_config(page_title=APP_TITLE, layout="wide")
st.markdown("<style>" + open("styles.css").read() + "</style>", unsafe_allow_html=True)

render_header()

menu = st.sidebar.radio(
    "Navigation",
    ["ATS Scanner", "Recruiter Mode", "Chat with Resume"]
)

# ATS SCANNER
if menu == "ATS Scanner":
    file, jd = render_upload_section()

    if st.button("🔍 Analyze Resume"):
        if file and jd:
            resume_text = extract_resume_text(file)
            st.session_state["resume_text"] = resume_text

            scores = ats_scores(resume_text, jd)
            analysis = analyze_resume(resume_text, jd)
            improved = improve_resume(resume_text, jd)

            render_ats_dashboard(scores, analysis, improved)

# RECRUITER MODE
elif menu == "Recruiter Mode":
    resume = st.session_state.get("resume_text", "")
    if resume:
        st.write(recruiter_evaluation(resume))
    else:
        st.warning("Upload a resume first in ATS Scanner.")

# CHAT WITH RESUME
elif menu == "Chat with Resume":
    resume = st.session_state.get("resume_text", "")
    if not resume:
        st.warning("Upload a resume first.")
    else:
        question = render_chat_section(resume)
        if question:
            st.write(chat_about_resume(resume, question))
