import streamlit as st
import docx2txt
from io import StringIO
import base64

st.set_page_config(page_title="ATS Resume Converter", layout="centered")

# --- Custom Styles ---
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stTextArea, .stTextInput, .stFileUploader, .stButton {
        font-size: 16px !important;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title & Instructions ---
st.title("🚀 ATS Resume Formatter")
st.subheader("Convert any resume into an ATS-compliant format with one click.")
st.markdown("💼 Upload your **.docx** resume using the drag & drop area below.")

# --- File Uploader ---
uploaded_file = st.file_uploader("📄 Upload Resume File (.docx)", type=["docx"], label_visibility="collapsed")

# --- Resume Processing Functions ---
def extract_text_from_docx(file):
    return docx2txt.process(file)

def convert_to_ats_format(text):
    ats_sections = {
        "Contact": "",
        "Education": "",
        "Experience": "",
        "Skills": "",
        "Projects": "",
        "Certifications": ""
    }

    lines = text.split('\n')
    current_section = "Contact"

    for line in lines:
        line = line.strip()
        if not line:
            continue

        header = line.lower()
        if "education" in header:
            current_section = "Education"
        elif "experience" in header or "work" in header:
            current_section = "Experience"
        elif "skill" in header:
            current_section = "Skills"
        elif "project" in header:
            current_section = "Projects"
        elif "certification" in header:
            current_section = "Certifications"
        else:
            ats_sections[current_section] += line + "\n"

    return ats_sections

# --- If File is Uploaded ---
if uploaded_file:
    st.success("✅ Resume uploaded successfully!")

    text = extract_text_from_docx(uploaded_file)
    ats_resume = convert_to_ats_format(text)

    st.markdown("### 📑 Preview of ATS-Formatted Resume")

    output_text = ""
    for section, content in ats_resume.items():
        st.markdown(f"#### ✦ {section}")
        st.text(content)
        output_text += f"===== {section.upper()} =====\n{content}\n"

    # --- Download Option ---
    st.download_button(
        label="⬇️ Download Clean ATS Resume (.txt)",
        data=output_text,
        file_name="ATS_Resume.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Drag and drop a .docx resume file to begin.")
