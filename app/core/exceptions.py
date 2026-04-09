"""Custom exceptions for contract processing failures."""

from fastapi import HTTPException, status


class ContractProcessingError(Exception):
    """Base exception for analysis pipeline errors."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_http_exception(self) -> HTTPException:
        """Convert the domain error into an HTTP exception."""

        return HTTPException(status_code=self.status_code, detail=self.message)


class UnsupportedFileTypeError(ContractProcessingError):
    """Raised when the uploaded file is neither PDF nor DOCX."""


class EmptyDocumentError(ContractProcessingError):
    """Raised when extraction yields no usable text."""


class InvalidCloudflareResponseError(ContractProcessingError):
    """Raised when the model response is missing required JSON fields."""
