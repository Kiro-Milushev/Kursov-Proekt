"""Validation helpers for incoming analysis requests."""

import re

from app.core.exceptions import ContractProcessingError

URL_PATTERN = re.compile(r"^https?://", re.IGNORECASE)
MIN_CONTEXT_LENGTH = 15


def validate_user_context(user_context: str) -> str:
    """Validate and normalize the user-provided role or context."""

    cleaned_context = user_context.strip()
    if len(cleaned_context) < MIN_CONTEXT_LENGTH:
        raise ContractProcessingError(
            f"User context must be at least {MIN_CONTEXT_LENGTH} characters long.",
        )
    if URL_PATTERN.match(cleaned_context):
        raise ContractProcessingError("User context must be pasted text, not a URL.")
    return cleaned_context
