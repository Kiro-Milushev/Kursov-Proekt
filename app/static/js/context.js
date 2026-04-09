"use strict";

const MIN_CONTEXT_LENGTH = 15;
const URL_PATTERN = /^https?:\/\//i;

const roleInput = document.getElementById("role-input");
const contextCounter = document.getElementById("context-counter");
const contextError = document.getElementById("context-error");
const scanButton = document.getElementById("scan-button");
const scanSpinner = document.getElementById("scan-spinner");
const scanArrow = document.getElementById("scan-arrow");
const currentUploadLabel = document.getElementById("current-upload-label");

const uploadId = sessionStorage.getItem("upload_id");
const uploadedFilename = sessionStorage.getItem("uploaded_filename");

if (!uploadId) {
  window.location.href = "/upload";
}

if (uploadedFilename) {
  currentUploadLabel.textContent = `Document: ${uploadedFilename}`;
}

function showContextError(message) {
  contextError.textContent = message;
  contextError.classList.remove("hidden");
}

function clearContextError() {
  contextError.textContent = "";
  contextError.classList.add("hidden");
}

function updateCounter() {
  const currentLength = roleInput.value.trim().length;
  contextCounter.textContent = `${currentLength} / ${MIN_CONTEXT_LENGTH}`;
}

function validateContext(value) {
  const trimmed = value.trim();
  if (trimmed.length < MIN_CONTEXT_LENGTH) {
    return `Role/context must be at least ${MIN_CONTEXT_LENGTH} characters.`;
  }
  if (URL_PATTERN.test(trimmed)) {
    return "URLs are not allowed. Paste your role/context as text.";
  }
  return null;
}

function setLoading(isLoading) {
  scanButton.disabled = isLoading;
  scanSpinner.classList.toggle("hidden", !isLoading);
  scanSpinner.classList.toggle("animate-spin", isLoading);
  scanArrow.classList.toggle("hidden", isLoading);
}

roleInput.addEventListener("input", () => {
  updateCounter();
  clearContextError();
});

scanButton.addEventListener("click", async () => {
  const userContext = roleInput.value;
  const validationError = validateContext(userContext);
  if (validationError) {
    showContextError(validationError);
    return;
  }

  setLoading(true);
  clearContextError();

  const formData = new FormData();
  formData.append("upload_id", uploadId);
  formData.append("user_context", userContext.trim());

  try {
    const response = await fetch("/analyze-upload", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Analysis failed.");
    }

    sessionStorage.setItem("analysis_result", JSON.stringify(payload));
    sessionStorage.removeItem("upload_id");
    window.location.href = "/result";
  } catch (error) {
    setLoading(false);
    showContextError(error.message || "Analysis failed. Please try again.");
  }
});

updateCounter();
