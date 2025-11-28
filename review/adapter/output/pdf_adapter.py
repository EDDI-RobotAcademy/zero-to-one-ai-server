from io import BytesIO
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

from review.application.port.pdf_port import PdfPort
from review.domain.pdf_document import PdfDocument

FONT_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../infrastructure/fonts/NanumGothic.ttf"
)
pdfmetrics.registerFont(TTFont("NanumGothic", FONT_PATH))

class PdfAdapter(PdfPort):

    def generate(self, document: PdfDocument) -> bytes:
        buffer = BytesIO()

        pdf = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        styles["Normal"].fontName = "NanumGothic"
        styles["Title"].fontName = "NanumGothic"
        story = []

        story.append(Paragraph(document.title, styles["Title"]))
        story.append(Spacer(1, 12))

        table_data = [
            [Paragraph("구분", styles["Normal"]), Paragraph("내용", styles["Normal"])],
            [Paragraph("상품명", styles["Normal"]), Paragraph(document.name, styles["Normal"])],
            [Paragraph("가격", styles["Normal"]), Paragraph(document.price, styles["Normal"])],
            [Paragraph("요약", styles["Normal"]), Paragraph(document.summary.replace('\n', '<br/>'), styles["Normal"])],
            [Paragraph("긍정 요인", styles["Normal"]), Paragraph(document.positive_features.replace('\n', '<br/>'), styles["Normal"])],
            [Paragraph("부정 요인", styles["Normal"]), Paragraph(document.negative_features.replace('\n', '<br/>'), styles["Normal"])],
            [Paragraph("키워드", styles["Normal"]), Paragraph(", ".join(document.keywords), styles["Normal"])],
        ]

        table = Table(table_data, colWidths=[80, 400], rowHeights=None)
        table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "NanumGothic"),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        story.append(table)
        story.append(Spacer(1, 24))

        pdf.build(story)
        return buffer.getvalue()