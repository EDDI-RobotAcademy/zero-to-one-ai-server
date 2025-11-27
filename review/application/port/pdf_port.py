from review.domain.pdf_document import PdfDocument

# PDF 파일 생성 기능
class PdfPort:
    # 도메인 객체를 받아 PDF 바이트 데이터로 생성
    def generate(self, document: PdfDocument) -> bytes:
        raise NotImplementedError

# 생성된 파일을 S3에 업로드
class StoragePort:
    # 파일명과 PDF 바이트 데이터를 받아 업로드 후 접근 가능한 URL 반환
    def upload(self, filename: str, file_bytes: bytes) -> str:
        raise NotImplementedError