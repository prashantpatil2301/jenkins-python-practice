from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def create_pdf():
    reports = Path(__file__).resolve().parent / "reports"

    log_file = reports / "output.txt"
    pdf_file = reports / "output.pdf"

    styles = getSampleStyleSheet()

    content = [
        Paragraph("Selenium Execution Report", styles["Title"]),
        Spacer(1, 12),
    ]

    for line in log_file.read_text(encoding="utf-8").splitlines():
        if line.strip():
            content.append(
                Paragraph(escape(line), styles["BodyText"])
            )
        else:
            content.append(Spacer(1, 6))

    document = SimpleDocTemplate(str(pdf_file), pagesize=A4)
    document.build(content)

    print(f"PDF saved to: {pdf_file}")