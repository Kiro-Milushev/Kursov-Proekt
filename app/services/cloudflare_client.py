"""Cloudflare AI client for contract analysis requests."""

import json

import httpx
from fastapi import status

from app.core.config import get_settings
from app.core.exceptions import ContractProcessingError, InvalidCloudflareResponseError


class CloudflareAIClient:
    """Encapsulate authenticated Cloudflare AI calls."""

    def __init__(self) -> None:
        self.settings = get_settings()

    async def run_analysis(self, prompt: str) -> dict[str, object]:
        """Send the prompt to Cloudflare and parse the JSON response."""

        self._ensure_configuration()
        headers = {
            "Authorization": f"Bearer {self.settings.cf_ai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "messages": [
                {"role": "system", "content": prompt},
            ]
        }

        try:
            async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
                response = await client.post(self.settings.cloudflare_ai_url, headers=headers, json=payload)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ContractProcessingError(
                "Cloudflare AI returned an error response.",
                status_code=status.HTTP_502_BAD_GATEWAY,
            ) from exc
        except httpx.HTTPError as exc:
            raise ContractProcessingError(
                "Unable to reach Cloudflare AI.",
                status_code=status.HTTP_502_BAD_GATEWAY,
            ) from exc

        data = response.json()
        content = self._extract_model_content(data)
        return self._parse_json_content(content)

    def _ensure_configuration(self) -> None:
        """Verify the Cloudflare configuration is present before calling the API."""

        if not self.settings.cf_account_id or not self.settings.cf_ai_api_key:
            raise ContractProcessingError(
                "Cloudflare configuration is missing.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def _extract_model_content(self, response_data: dict[str, object]) -> str:
        """Extract the raw text payload from the Cloudflare response."""

        try:
            result = response_data["result"]
            if not isinstance(result, dict):
                raise KeyError("result")
            response = result["response"]
            if isinstance(response, str):
                return response
        except KeyError as exc:
            raise InvalidCloudflareResponseError("Cloudflare response is missing the expected result payload.") from exc

        raise InvalidCloudflareResponseError("Cloudflare response did not include a text response.")

    def _parse_json_content(self, content: str) -> dict[str, object]:
        """Parse the model's JSON string into a dictionary."""

        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            cleaned_content = self._extract_json_object(content)
            try:
                parsed = json.loads(cleaned_content)
            except json.JSONDecodeError as inner_exc:
                raise InvalidCloudflareResponseError("The model returned invalid JSON.") from inner_exc

        if not isinstance(parsed, dict):
            raise InvalidCloudflareResponseError("The model response must be a JSON object.")

        return parsed

    def _extract_json_object(self, content: str) -> str:
        """Extract a likely JSON object from fenced or mixed model output."""

        stripped = content.strip()
        if stripped.startswith("```"):
            stripped = stripped.removeprefix("```json").removeprefix("```").strip()
            if stripped.endswith("```"):
                stripped = stripped[:-3].strip()

        start_index = stripped.find("{")
        end_index = stripped.rfind("}")
        if start_index != -1 and end_index != -1 and end_index > start_index:
            return stripped[start_index : end_index + 1]

        return stripped
