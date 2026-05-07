import pdfplumber

from app.utils.file_helpers import bytes_to_spooled_file, normalize_whitespace


def extract_pdf_text(contents: bytes) -> tuple[str, int]:
    with bytes_to_spooled_file(contents) as pdf_file:
        with pdfplumber.open(pdf_file) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
            return normalize_whitespace("\n".join(pages)), len(pdf.pages)
