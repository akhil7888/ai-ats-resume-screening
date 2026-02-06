import streamlit as st
import plotly.graph_objects as go

def render_header():
    st.markdown("""
        <div class="header">
            <h1>AI ATS Resume Screening</h1>
            <p class="subtitle">Built by Akhil Ch · Powered by Groq · Modern AI Technology</p>
        </div>
    """, unsafe_allow_html=True)


def render_upload_section():
    st.markdown("<h3 class='section-title'>📄 Upload Resume & Job Description</h3>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        resume_file = st.file_uploader("Upload Resume (PDF / DOCX)", type=["pdf", "docx"])
    with col2:
        jd_text = st.text_area("Paste Job Description", height=150)

    return resume_file, jd_text


def render_ats_dashboard(scores, analysis, improved):
    st.markdown("<h3 class='section-title'>📊 ATS Summary</h3>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("ATS Match", f"{scores['match']}%")
    c2.metric("Job Fit", f"{scores['fit']}%")
    c3.metric("Quality Score", f"{scores['quality']}%")

    # Radar chart
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[scores['match'], scores['fit'], scores['quality']],
        theta=["ATS Match", "Job Fit", "Quality"],
        fill="toself"
    ))
    fig.update_layout(height=350, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Skill Gaps
    st.markdown("<h3 class='section-title'>🧩 Skill Gap Matrix</h3>", unsafe_allow_html=True)
    st.dataframe(scores["skill_gaps"], use_container_width=True)

    # AI Analysis
    st.markdown("<h3 class='section-title'>🧠 AI Resume Evaluation</h3>", unsafe_allow_html=True)
    st.markdown(f"<div class='card'>{analysis}</div>", unsafe_allow_html=True)

    # Improved Resume
    st.markdown("<h3 class='section-title'>✨ Improved Resume</h3>", unsafe_allow_allow_html=True)
    st.markdown(f"<div class='card'>{improved}</div>", unsafe_allow_html=True)


def render_chat_section():
    st.markdown("<h3 class='section-title'>💬 Chat with Resume</h3>", unsafe_allow_html=True)
    resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    if resume:
        from utils import extract_text, chat_with_resume
        resume_text = extract_text(resume)
        query = st.text_input("Ask something about the resume")

        if query:
            resp = chat_with_resume(resume_text, query)
            st.markdown(f"<div class='card'>{resp}</div>", unsafe_allow_html=True)


def render_jd_generator():
    st.markdown("<h3 class='section-title'>📝 Job Description Generator</h3>", unsafe_allow_html=True)
    role = st.text_input("Job Title")

    if st.button("Generate JD"):
        from utils import generate_jd
        jd = generate_jd(role)
        st.markdown(f"<div class='card'>{jd}</div>", unsafe_allow_html=True)


def render_recruiter_mode():
    st.markdown("<h3 class='section-title'>🏆 Recruiter Mode — Rank Multiple Resumes</h3>", unsafe_allow_html=True)

    resumes = st.file_uploader("Upload Multiple Resumes", accept_multiple_files=True)
    jd = st.text_area("Job Description")

    if st.button("Rank Candidates"):
        from recruiter import rank_resumes
        df = rank_resumes(resumes, jd)
        st.dataframe(df, use_container_width=True)
