import gradio as gr
from utils import (
    extract_text,
    ats_scores,
    analyze_resume,
    improve_resume,
    generate_jd,
    recruiter_evaluation,
    chat_with_resume
)
from config import APP_TITLE


# --------------------------------
# ATS Scanner Function
# --------------------------------
def run_ats_scanner(file, jd):
    resume_text = extract_text(file)
    scores = ats_scores(resume_text, jd)
    analysis = analyze_resume(resume_text, jd)
    improved = improve_resume(resume_text, jd)
    return (
        scores["match"],
        scores["fit"],
        scores["quality"],
        analysis,
        improved,
        resume_text
    )


# --------------------------------
# JD Generator
# --------------------------------
def run_jd(role):
    return generate_jd(role)


# --------------------------------
# Recruiter Mode
# --------------------------------
def run_recruiter(resume):
    return recruiter_evaluation(resume)


# --------------------------------
# Chat With Resume
# --------------------------------
def run_chat(resume, question):
    if not resume:
        return "Upload and scan resume first."
    return chat_with_resume(resume, question)


# --------------------------------
# GRADIO UI
# --------------------------------
with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft()) as app:

    gr.Markdown(f"# 📄 {APP_TITLE}")
    gr.Markdown("Powered by **Groq + Gradio**")

    # Hidden state to store resume text
    resume_state = gr.State("")

    with gr.Tabs():

        # -------------------------
        # ATS SCANNER TAB
        # -------------------------
        with gr.Tab("ATS Scanner"):
            file = gr.File(label="Upload Resume (PDF / DOCX)")
            jd = gr.Textbox(label="Paste Job Description", lines=6)
            analyze_btn = gr.Button("🔍 Analyze Resume")

            match = gr.Number(label="ATS Match %")
            fit = gr.Number(label="Job Fit %")
            quality = gr.Number(label="Resume Quality %")

            analysis = gr.Textbox(label="ATS Analysis", lines=6)
            improved = gr.Textbox(label="Improved Resume", lines=10)

            analyze_btn.click(
                run_ats_scanner,
                inputs=[file, jd],
                outputs=[match, fit, quality, analysis, improved, resume_state]
            )

        # -------------------------
        # JD GENERATOR TAB
        # -------------------------
        with gr.Tab("JD Generator"):
            role = gr.Textbox(label="Enter Job Role")
            jd_btn = gr.Button("Generate JD")
            jd_out = gr.Textbox(label="Generated Job Description", lines=10)

            jd_btn.click(run_jd, inputs=[role], outputs=[jd_out])

        # -------------------------
        # RECRUITER MODE TAB
        # -------------------------
        with gr.Tab("Recruiter Mode"):
            recruiter_btn = gr.Button("Evaluate Resume")
            recruiter_out = gr.Textbox(label="Recruiter Feedback", lines=10)

            recruiter_btn.click(run_recruiter, inputs=[resume_state], outputs=[recruiter_out])

        # -------------------------
        # CHAT WITH RESUME TAB
        # -------------------------
        with gr.Tab("Chat With Resume"):
            question = gr.Textbox(label="Ask a question about the resume")
            chat_btn = gr.Button("Ask")
            chat_out = gr.Textbox(label="Answer", lines=5)

            chat_btn.click(run_chat, inputs=[resume_state, question], outputs=[chat_out])


app.launch()
