"""Orchestrates the end-to-end contract analysis workflow."""

from io import BytesIO

from fastapi import UploadFile
from starlette.datastructures import UploadFile as StarletteUploadFile

from app.core.exceptions import EmptyDocumentError
from app.schemas.analysis import AnalysisResponse
from app.schemas.prompt import ContractAnalysisInput
from app.services.cloudflare_client import CloudflareAIClient
from app.services.document_extractor import extract_contract_text
from app.services.input_validation import validate_user_context
from app.services.prompt_builder import build_contract_prompt


async def analyze_contract(contract_file: UploadFile, user_context: str) -> AnalysisResponse:
    """Validate, extract, prompt, and analyze a contract upload."""

    normalized_context = validate_user_context(user_context)
    extracted_text = await extract_contract_text(contract_file)
    if not extracted_text.strip():
        raise EmptyDocumentError("The uploaded document does not contain readable text.")

    analysis_input = ContractAnalysisInput(
        user_context=normalized_context,
        contract_text=extracted_text.strip(),
    )
    prompt = build_contract_prompt(analysis_input)
    client = CloudflareAIClient()
    model_output = await client.run_analysis(prompt)
    return AnalysisResponse(**model_output)


async def analyze_contract_bytes(filename: str, content: bytes, user_context: str) -> AnalysisResponse:
    """Analyze a contract from in-memory file content and filename."""

    upload_file = StarletteUploadFile(file=BytesIO(content), filename=filename)
    return await analyze_contract(contract_file=upload_file, user_context=user_context)
