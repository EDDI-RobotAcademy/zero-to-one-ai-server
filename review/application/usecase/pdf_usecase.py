# PDF 생성과 S3 업로드 과정을 순차적으로 실행하
from datetime import datetime

class PdfUseCase:
    def __init__(self, pdf_port, storage_port):
        self.pdf_port = pdf_port
        self.storage_port = storage_port

    # PDF 생성 후 S3 업로드하고 접근 가능한 URL 반환
    def execute(self, summary_vo):
        pdf_bytes = self.pdf_port.generate(summary_vo)
        filename = f"review-summary-{datetime.utcnow().timestamp()}.pdf"
        s3_url = self.storage_port.upload(filename, pdf_bytes)

        return {
            "filename": filename,
            "url": s3_url
        }