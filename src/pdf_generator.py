from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(report_data, filename):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Placement Report")

    # Add report data
    p.setFont("Helvetica", 12)
    y_position = height - 100
    for key, value in report_data.items():
        p.drawString(100, y_position, f"{key}: {value}")
        y_position -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    with open(filename, 'wb') as f:
        f.write(buffer.read()) 