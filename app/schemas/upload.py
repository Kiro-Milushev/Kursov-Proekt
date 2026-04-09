"""Schemas for temporary upload session responses."""

from pydantic import BaseModel


class UploadSessionResponse(BaseModel):
    """Response returned after storing an uploaded contract file."""

    upload_id: str
    filename: str
