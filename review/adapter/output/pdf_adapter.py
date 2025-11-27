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
            ["구분", "내용"],
            ["상품명", document.product_name],
            ["가격", document.price],
            ["카테고리", document.category],
            ["요약", document.summary],
            ["긍정 요인", document.positive_features],
            ["부정 요인", document.negative_features],
            ["키워드", ", ".join(document.keywords)],
        ]

        table = Table(table_data, colWidths=[80, 400])
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