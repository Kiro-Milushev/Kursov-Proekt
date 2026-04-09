# ContractClear AI

ContractClear AI is a FastAPI web app that analyzes contract risk with a Cloudflare-hosted LLM.

It accepts PDF/DOCX files plus user role/context and returns:
- `risk_score` (0-10)
- `red_flags` (list of risky clauses)
- `summary` (plain-language explanation)

## Stack

- Backend: FastAPI, Pydantic, httpx
- AI: Cloudflare AI (`@cf/meta/llama-3.2-3b-instruct` by default)
- Document parsing: PyPDF2, python-docx
- Frontend: HTML, Tailwind CSS, vanilla JavaScript

## Quick Start (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Configure environment variables:

```powershell
Copy-Item .env.example .env
```

4. Ensure `.env` contains valid Cloudflare credentials.
Required:
- `CF_ACCOUNT_ID`
- `CF_AI_API_KEY`

Optional:
- `CF_MODEL` (default: `@cf/meta/llama-3.2-3b-instruct`)
- `REQUEST_TIMEOUT_SECONDS` (default: `90.0`)

5. Run the app:

```powershell
uvicorn app.main:app --reload
```

Open:
- UI: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`

## User Flow

1. Upload a contract (`.pdf` or `.docx`).
2. Provide role/context (minimum 15 characters, URLs blocked).
3. Receive risk score, red flags, and summary.

## API Endpoints

- `GET /health` - readiness check
- `POST /upload-document` - upload file and get `upload_id`
- `POST /analyze-upload` - analyze uploaded file using `upload_id` + `user_context`
- `POST /analyze` - single request with `contract_file` + `user_context`

## Project Structure

- `app/main.py` - app entrypoint and page routes
- `app/api/routes.py` - HTTP routes
- `app/services/` - extraction, validation, prompting, AI client, upload store
- `app/schemas/` - request/response schemas
- `app/static/` - frontend pages and JavaScript

## Notes

- If Cloudflare credentials are missing or invalid, analysis calls fail.
- Uploaded files are stored in-memory temporarily for the upload/context/result flow.


