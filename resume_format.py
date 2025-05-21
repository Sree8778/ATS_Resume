import streamlit as st
from fpdf import FPDF
import re

def generate_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", size=12)

    safe_content = re.sub(r'(\S{80,})', r'\1 ', content)
    for line in safe_content.split('\n'):
        pdf.multi_cell(190, 8, line.strip())
    pdf.output(filename)
    return filename

def format_resume(data):
    resume_text = f"""
{data['name'].upper()}
{data['contact']} | {data['email']} | {data['linkedin']} | {data['location']}

{data['title'].upper()}
{data['summary']}

WORK EXPERIENCE"""
    for job in data['jobs']:
        resume_text += f"\n{job['company']}\n{job['title']} ({job['dates']})"
        for point in job['points']:
            resume_text += f"\n- {point}"

    resume_text += "\n\nEDUCATION"
    for edu in data['education']:
        resume_text += f"\n{edu['school']} ({edu['date']})\n{edu['degree']}"
        for detail in edu['details']:
            resume_text += f"\n- {detail}"

    resume_text += "\n\nPROJECTS"
    for proj in data['projects']:
        resume_text += f"\n{proj['title']} ({proj['tech']})"
        for desc in proj['descriptions']:
            resume_text += f"\n- {desc}"

    resume_text += "\n\nSKILLS"
    for skill in data['skills']:
        resume_text += f"\n- {skill}"

    return resume_text.strip()

def extract_text_from_pdf(uploaded_file):
    from PyPDF2 import PdfReader
    reader = PdfReader(uploaded_file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

def extract_text_from_docx(uploaded_file):
    from docx import Document
    doc = Document(uploaded_file)
    return "\n".join([para.text for para in doc.paragraphs])

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def get_dynamic_entries(section_name, entry_label, max_entries, point_label, key_prefix):
    count = st.number_input(f"How many {section_name}? (max {max_entries})", min_value=1, max_value=max_entries, value=1, key=f"{key_prefix}_count")
    entries = []
    for i in range(count):
        st.markdown(f"**{entry_label} #{i+1}**")
        if section_name == "jobs":
            company = st.text_input("Company Name", key=f"{key_prefix}_company_{i}")
            title = st.text_input("Job Title", key=f"{key_prefix}_title_{i}")
            dates = st.text_input("Dates", key=f"{key_prefix}_dates_{i}")
            points = get_dynamic_points(point_label, f"{key_prefix}_points_{i}", max_points=4)
            entries.append({"company": company, "title": title, "dates": dates, "points": points})
        elif section_name == "education":
            school = st.text_input("School Name", key=f"{key_prefix}_school_{i}")
            degree = st.text_input("Degree", key=f"{key_prefix}_degree_{i}")
            date = st.text_input("Date", key=f"{key_prefix}_date_{i}")
            details = get_dynamic_points("Education Detail", f"{key_prefix}_detail_{i}", max_points=4)
            entries.append({"school": school, "degree": degree, "date": date, "details": details})
        elif section_name == "projects":
            title = st.text_input("Project Title", key=f"{key_prefix}_title_{i}")
            tech = st.text_input("Tech/Stack", key=f"{key_prefix}_tech_{i}")
            descriptions = get_dynamic_points("Project Description", f"{key_prefix}_desc_{i}", max_points=4)
            entries.append({"title": title, "tech": tech, "descriptions": descriptions})
        elif section_name == "skills":
            skill = st.text_input("Skill", key=f"{key_prefix}_skill_{i}")
            entries.append(skill)
    return entries

def get_dynamic_points(section_label, key_prefix, max_points=4):
    num_points = st.number_input(
        f"How many bullet points for {section_label}? (max {max_points})",
        min_value=1, max_value=max_points, value=1, step=1,
        key=f"{key_prefix}_num"
    )
    points = []
    for i in range(num_points):
        point = st.text_input(f"• Point {i+1} for {section_label}", key=f"{key_prefix}_point{i}")
        points.append(point)
    return points

st.set_page_config(page_title="ATS Resume Builder", layout="centered")
st.title("📄 ATS-Friendly Resume Generator")

option = st.radio(
    "Choose how you'd like to create your resume:",
    ("Manual Form Input", "Upload Resume File (Non-Formatted)")
)

if option == "Upload Resume File (Non-Formatted)":
    st.subheader("📤 Upload Resume File")
    uploaded_file = st.file_uploader("Upload a PDF or DOCX resume", type=["pdf", "docx"])
    if uploaded_file:
        if uploaded_file.name.endswith(".pdf"):
            raw_text = extract_text_from_pdf(uploaded_file)
        else:
            raw_text = extract_text_from_docx(uploaded_file)
        cleaned_text = clean_text(raw_text)
        st.text_area("📋 Extracted Resume Text (read-only)", cleaned_text, height=200)

st.markdown("---")

st.subheader("👤 Basic Info")
name = st.text_input("Full Name", key="name")
email = st.text_input("Email", key="email")
contact = st.text_input("Phone Number", key="contact")
linkedin = st.text_input("LinkedIn URL", key="linkedin")
location = st.text_input("Location (City, State)", key="location")

title = st.text_input("Job Title (e.g. Creative Director)", key="title")
summary = st.text_area("Brief Summary About You", height=100, key="summary")

st.subheader("💼 Work Experience")
jobs = get_dynamic_entries("jobs", "Job", 4, "Responsibility", "job")

st.subheader("🎓 Education")
education = get_dynamic_entries("education", "Education Entry", 4, "Detail", "edu")

st.subheader("🧪 Projects")
projects = get_dynamic_entries("projects", "Project", 4, "Project Detail", "proj")

st.subheader("🛠 Skills")
skills = get_dynamic_entries("skills", "Skill", 4, "", "skill")

if st.button("📄 Generate ATS Resume"):
    if not name:
        st.error("Please enter your name.")
    else:
        inputs = {
            "name": name,
            "email": email,
            "contact": contact,
            "linkedin": linkedin,
            "location": location,
            "title": title,
            "summary": summary,
            "jobs": jobs,
            "education": education,
            "projects": projects,
            "skills": skills
        }

        final_resume = format_resume(inputs)
        file_basename = name.strip().lower().replace(" ", "_") + "_ATSresume"

        st.subheader("📋 Resume Preview")
        st.text_area("Formatted Resume Output", final_resume, height=400)

        pdf_path = f"{file_basename}.pdf"
        generate_pdf(final_resume, pdf_path)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download as PDF",
                data=f,
                file_name=pdf_path,
                mime="application/pdf"
            )
