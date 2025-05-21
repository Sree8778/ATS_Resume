import os
import fitz  # PyMuPDF
import docx2txt
from fpdf import FPDF
from pathlib import Path
from zipfile import ZipFile

def extract_text(file_path):
    ext = file_path.suffix.lower()
    try:
        if ext == ".docx":
            return docx2txt.process(file_path)
        elif ext == ".pdf":
            with fitz.open(file_path) as pdf:
                return "".join(page.get_text() for page in pdf)
    except Exception as e:
        print(f"❌ Failed to extract from {file_path.name}: {e}")
    return ""

def convert_to_ats_format(text):
    sections = {
        "Contact": "", "Education": "", "Experience": "",
        "Skills": "", "Projects": "", "Certifications": ""
    }
    current_section = "Contact"
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        tag = line.lower()
        if "education" in tag:
            current_section = "Education"
        elif "experience" in tag or "work" in tag:
            current_section = "Experience"
        elif "skill" in tag:
            current_section = "Skills"
        elif "project" in tag:
            current_section = "Projects"
        elif "certification" in tag:
            current_section = "Certifications"
        else:
            sections[current_section] += line + "\n"
    return sections

def create_pdf_from_sections(sections, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for section, content in sections.items():
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(0, 10, f"{section.upper()}", ln=True)
        pdf.set_font("Arial", style="", size=12)
        for line in content.splitlines():
            pdf.multi_cell(0, 10, line)
        pdf.ln()
    try:
        pdf.output(str(output_path))
        print(f"✅ PDF saved: {output_path.name}")
    except Exception as e:
        print(f"❌ Error saving PDF: {e}")

def process_resumes(input_folder, output_zip):
    input_path = Path(input_folder)
    output_dir = input_path.parent / "processed_pdfs"
    output_dir.mkdir(exist_ok=True)

    pdf_paths = []
    resume_count = 0

    for filepath in input_path.rglob("*"):
        if filepath.suffix.lower() in [".pdf", ".docx"]:
            print(f"📄 Found file: {filepath.name}")
            text = extract_text(filepath)
            if not text.strip():
                print(f"⚠️ No text extracted from: {filepath.name} — skipping")
                continue

            ats_data = convert_to_ats_format(text)
            pdf_name = filepath.stem + "_ATS.pdf"
            pdf_output_path = output_dir / pdf_name
            create_pdf_from_sections(ats_data, pdf_output_path)

            if pdf_output_path.exists():
                pdf_paths.append(pdf_output_path)
                resume_count += 1
            else:
                print(f"❌ PDF not created: {pdf_output_path}")

    if resume_count == 0:
        print("🚫 No valid resumes were processed.")
    else:
        with ZipFile(output_zip, 'w') as zipf:
            for file in pdf_paths:
                if file.exists():
                    zipf.write(file, arcname=file.name)
                else:
                    print(f"⚠️ Skipping missing file: {file}")
        print(f"📦 ATS resumes zipped: {output_zip}")
