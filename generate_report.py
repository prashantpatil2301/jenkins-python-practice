from pathlib import Path
from reportlab.pdfgen import canvas

report = (
    "Prashant's Jenkins Pipeline - Version 2\n"
    "Code fetched from GitHub.\n"
    "Python script executed inside Docker.\n"
    "TXT and PDF reports generated successfully.\n"
)

output_folder = Path(__file__).resolve().parent / "reports"
output_folder.mkdir(exist_ok=True)

output_file = output_folder / "output.txt"
output_file.write_text(report, encoding="utf-8")

print(report)
print(f"Report saved to: {output_file}")

pdf_file = output_folder / "output.pdf"

pdf = canvas.Canvas(str(pdf_file))
pdf.setFont("Helvetica", 12)

y_position = 800

for line in report.splitlines():
    pdf.drawString(50, y_position, line)
    y_position -= 20

pdf.save()

print(f"PDF saved to: {pdf_file}")