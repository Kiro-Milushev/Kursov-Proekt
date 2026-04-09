"""Document text extraction for PDF and DOCX uploads."""

from io import BytesIO
from zipfile import BadZipFile

from docx import Document
from fastapi import UploadFile
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

from app.core.exceptions import ContractProcessingError, UnsupportedFileTypeError

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


async def extract_contract_text(contract_file: UploadFile) -> str:
    """Extract text from the uploaded contract document."""

    file_name = contract_file.filename or ""
    extension = f".{file_name.lower().rsplit('.', maxsplit=1)[-1]}" if "." in file_name else ""
    if extension not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError("Only PDF and DOCX files are supported.")

    file_bytes = await contract_file.read()
    if extension == ".pdf":
        return _extract_pdf_text(file_bytes)
    return _extract_docx_text(file_bytes)


def _extract_pdf_text(file_bytes: bytes) -> str:
    """Extract text from a PDF file."""

    try:
        reader = PdfReader(BytesIO(file_bytes))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n".join(pages)
    except PdfReadError as exc:
        raise ContractProcessingError("The uploaded PDF is invalid or corrupted.") from exc


def _extract_docx_text(file_bytes: bytes) -> str:
    """Extract text from a DOCX file."""

    try:
        document = Document(BytesIO(file_bytes))
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text]
        return "\n".join(paragraphs)
    except (BadZipFile, ValueError) as exc:
        raise ContractProcessingError("The uploaded DOCX file is invalid or corrupted.") from exc
