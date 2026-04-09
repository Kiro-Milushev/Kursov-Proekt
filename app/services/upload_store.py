"""Temporary in-memory storage for uploaded contract files."""

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import secrets

from app.core.exceptions import ContractProcessingError

UPLOAD_TTL_MINUTES = 30


@dataclass(slots=True)
class StoredUpload:
    """Container for a temporarily stored uploaded file."""

    upload_id: str
    filename: str
    content: bytes
    created_at: datetime


_UPLOADS: dict[str, StoredUpload] = {}


def save_upload(filename: str, content: bytes) -> str:
    """Save an uploaded file and return a short-lived upload identifier."""

    _purge_expired_uploads()
    upload_id = secrets.token_urlsafe(18)
    _UPLOADS[upload_id] = StoredUpload(
        upload_id=upload_id,
        filename=filename,
        content=content,
        created_at=datetime.now(tz=timezone.utc),
    )
    return upload_id


def get_upload(upload_id: str) -> StoredUpload:
    """Get a stored upload by ID or raise a domain error if missing."""

    _purge_expired_uploads()
    stored_upload = _UPLOADS.get(upload_id)
    if stored_upload is None:
        raise ContractProcessingError("Uploaded document session has expired. Please upload again.")
    return stored_upload


def remove_upload(upload_id: str) -> None:
    """Delete a stored upload by ID if it exists."""

    _UPLOADS.pop(upload_id, None)


def _purge_expired_uploads() -> None:
    """Remove uploads that exceeded the configured in-memory lifetime."""

    now = datetime.now(tz=timezone.utc)
    expiration_threshold = now - timedelta(minutes=UPLOAD_TTL_MINUTES)
    expired_keys = [
        key
        for key, value in _UPLOADS.items()
        if value.created_at < expiration_threshold
    ]
    for key in expired_keys:
        _UPLOADS.pop(key, None)
