from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas

def export_ats_to_pdf(ats_data, output_path):
    c = canvas.Canvas(output_path, pagesize=LETTER)
    width, height = LETTER
    y = height - 50
    line_height = 15

    def draw_section(title, content):
        nonlocal y
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, title.upper())
        y -= line_height
        c.setFont("Helvetica", 10)
        if isinstance(content, list):
            for item in content:
                for line in item.splitlines():
                    c.drawString(60, y, f"• {line}")
                    y -= line_height
        else:
            for line in content.splitlines():
                c.drawString(60, y, line)
                y -= line_height
        y -= 10

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, ats_data["Name"])
    y -= line_height
    c.setFont("Helvetica", 10)
    c.drawString(50, y, ats_data["Contact"])
    y -= 20

    for section in ["Summary", "Skills", "Experience", "Education", "Certifications", "Projects"]:
        if ats_data[section]:
            draw_section(section, ats_data[section])

    c.save()
