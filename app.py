import streamlit as st
import tempfile
import os

from extract_text import extract_text_from_docx, extract_text_from_pdf
from format_ats import format_ats_resume
from export_pdf import export_ats_to_pdf

st.set_page_config(page_title="ATS Resume Builder", layout="centered")
st.title("📄 ATS Resume Builder")

choice = st.radio("Choose an Option", ["Upload Resume", "Create New Resume from Scratch"])

# ----------------------- UPLOAD MODE -----------------------
if choice == "Upload Resume":
    uploaded_file = st.file_uploader("Upload a .docx or .pdf resume", type=["docx", "pdf"])

    if uploaded_file:
        file_ext = uploaded_file.name.split(".")[-1]
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_ext}") as temp:
            temp.write(uploaded_file.read())
            file_path = temp.name

        st.info("📥 Resume uploaded successfully. Extracting content...")

        if file_ext == "docx":
            raw_text = extract_text_from_docx(file_path)
        else:
            raw_text = extract_text_from_pdf(file_path)

        st.text_area("🧾 Extracted Resume Text", raw_text, height=300)

        ats_resume = format_ats_resume(
            name="Candidate Name",
            contact="Email | Phone | LinkedIn | Location",
            summary="Summary extracted from resume or default fallback.",
            skills=["Adaptability", "Problem-Solving", "Team Collaboration"],
            experiences=[raw_text],
            education=["Education not detected."],
            certs=["None provided."],
            projects=["Not listed."]
        )

        output_path = os.path.join(tempfile.gettempdir(), "ATS_Resume_Uploaded.pdf")
        export_ats_to_pdf(ats_resume, output_path)

        with open(output_path, "rb") as f:
            st.success("✅ ATS resume formatted successfully.")
            st.download_button(
                label="📥 Download Formatted Resume (PDF)",
                data=f.read(),
                file_name="ATS_Resume.pdf",
                mime="application/pdf"
            )

# ----------------------- CREATE MODE -----------------------
elif choice == "Create New Resume from Scratch":
    st.header("📝 Build Your ATS Resume")

    with st.form("resume_form"):
        name = st.text_input("Full Name")
        contact = st.text_input("Contact (Phone | Email | LinkedIn | Location)")
        summary = st.text_area("Professional Summary", height=100)
        skills = st.text_area("Skills (comma-separated)")

        st.subheader("Experience")
        job_title = st.text_input("Job Title")
        company = st.text_input("Company")
        duration = st.text_input("Duration")
        job_desc = st.text_area("Job Description (one bullet per line)", height=100)

        st.subheader("Education")
        education = st.text_area("Education Details", height=80)

        st.subheader("Certifications")
        certs = st.text_area("Certifications (one per line)", height=60)

        st.subheader("Projects")
        projects = st.text_area("Projects (one per line)", height=80)

        submitted = st.form_submit_button("🎯 Generate ATS Resume")

    if submitted:
        resume_data = format_ats_resume(
            name=name,
            contact=contact,
            summary=summary,
            skills=[s.strip() for s in skills.split(",") if s.strip()],
            experiences=[f"{job_title} – {company} – {duration}", job_desc],
            education=[education],
            certs=[c.strip() for c in certs.splitlines() if c.strip()],
            projects=[p.strip() for p in projects.splitlines() if p.strip()]
        )

        output_path = os.path.join(tempfile.gettempdir(), f"{name.replace(' ', '_')}_ATS.pdf")
        export_ats_to_pdf(resume_data, output_path)

        with open(output_path, "rb") as f:
            st.success("✅ Your ATS resume is ready!")
            st.download_button(
                label="📥 Download ATS Resume (PDF)",
                data=f.read(),
                file_name=f"{name.replace(' ', '_')}_ATS_Resume.pdf",
                mime="application/pdf"
            )
