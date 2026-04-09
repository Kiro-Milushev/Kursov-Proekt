"""Prompt-related schema helpers."""

from pydantic import BaseModel


class ContractAnalysisInput(BaseModel):
    """Normalized analysis input sent to the prompt builder."""

    user_context: str
    contract_text: str
