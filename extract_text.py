from docx import Document
import fitz

def extract_text_from_docx(path):
    try:
        doc = Document(path)
        return "\n".join(p.text.strip() for p in doc.paragraphs if p.text.strip())
    except Exception as e:
        return f"Error reading DOCX: {e}"

def extract_text_from_pdf(path):
    try:
        with fitz.open(path) as doc:
            return "".join(page.get_text() for page in doc if page.get_text().strip())
    except Exception as e:
        return f"Error reading PDF: {e}"
