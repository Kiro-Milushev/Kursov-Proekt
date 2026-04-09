"""HTTP routes for contract analysis requests."""

from fastapi import APIRouter, File, Form, UploadFile

from app.core.exceptions import ContractProcessingError
from app.schemas.analysis import AnalysisResponse
from app.schemas.upload import UploadSessionResponse
from app.services.analysis_service import analyze_contract, analyze_contract_bytes
from app.services.upload_store import get_upload, remove_upload, save_upload

router = APIRouter(tags=["analysis"])


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Return a basic health response for readiness checks."""

    return {"status": "ok"}


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze(
    contract_file: UploadFile = File(...),
    user_context: str = Form(...),
) -> AnalysisResponse:
    """Analyze an uploaded contract against the user's context."""

    try:
        return await analyze_contract(contract_file=contract_file, user_context=user_context)
    except ContractProcessingError as exc:
        raise exc.to_http_exception() from exc


@router.post("/upload-document", response_model=UploadSessionResponse)
async def upload_document(contract_file: UploadFile = File(...)) -> UploadSessionResponse:
    """Store an uploaded file temporarily and return a short-lived token."""

    try:
        content = await contract_file.read()
        upload_id = save_upload(filename=contract_file.filename or "document", content=content)
        return UploadSessionResponse(upload_id=upload_id, filename=contract_file.filename or "document")
    except ContractProcessingError as exc:
        raise exc.to_http_exception() from exc


@router.post("/analyze-upload", response_model=AnalysisResponse)
async def analyze_upload(upload_id: str = Form(...), user_context: str = Form(...)) -> AnalysisResponse:
    """Analyze a previously uploaded file using a temporary upload token."""

    try:
        stored_upload = get_upload(upload_id)
        result = await analyze_contract_bytes(
            filename=stored_upload.filename,
            content=stored_upload.content,
            user_context=user_context,
        )
        remove_upload(upload_id)
        return result
    except ContractProcessingError as exc:
        raise exc.to_http_exception() from exc
