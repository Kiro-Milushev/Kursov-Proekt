"use strict";

const MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024;
const ALLOWED_EXTENSIONS = ["pdf", "docx"];

const fileInput = document.getElementById("file-upload");
const proceedButton = document.getElementById("proceed-button");
const uploadError = document.getElementById("upload-error");
const selectedFileLabel = document.getElementById("selected-file-label");

let selectedFile = null;

function showUploadError(message) {
  uploadError.textContent = message;
  uploadError.classList.remove("hidden");
}

function clearUploadError() {
  uploadError.textContent = "";
  uploadError.classList.add("hidden");
}

function getFileExtension(name) {
  const parts = name.toLowerCase().split(".");
  return parts.length > 1 ? parts.pop() : "";
}

function validateFile(file) {
  const extension = getFileExtension(file.name);
  if (!ALLOWED_EXTENSIONS.includes(extension)) {
    return "Only PDF and DOCX files are allowed.";
  }
  if (file.size > MAX_FILE_SIZE_BYTES) {
    return "File size must be 25MB or smaller.";
  }
  return null;
}

function setProceedEnabled(enabled) {
  proceedButton.disabled = !enabled;
  proceedButton.classList.toggle("cursor-not-allowed", !enabled);
  proceedButton.classList.toggle("text-on-surface-variant/50", !enabled);
  proceedButton.classList.toggle("bg-outline-variant/30", !enabled);
  proceedButton.classList.toggle("bg-primary", enabled);
  proceedButton.classList.toggle("text-on-primary", enabled);
}

fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files && fileInput.files[0] ? fileInput.files[0] : null;
  clearUploadError();

  if (!selectedFile) {
    selectedFileLabel.classList.add("hidden");
    setProceedEnabled(false);
    return;
  }

  const validationError = validateFile(selectedFile);
  if (validationError) {
    showUploadError(validationError);
    selectedFile = null;
    selectedFileLabel.classList.add("hidden");
    setProceedEnabled(false);
    return;
  }

  selectedFileLabel.textContent = `Selected: ${selectedFile.name}`;
  selectedFileLabel.classList.remove("hidden");
  setProceedEnabled(true);
});

proceedButton.addEventListener("click", async () => {
  if (!selectedFile) {
    return;
  }

  clearUploadError();
  proceedButton.disabled = true;

  const formData = new FormData();
  formData.append("contract_file", selectedFile);

  try {
    const response = await fetch("/upload-document", {
      method: "POST",
      body: formData,
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "Upload failed.");
    }

    sessionStorage.setItem("upload_id", payload.upload_id);
    sessionStorage.setItem("uploaded_filename", payload.filename);
    window.location.href = "/context";
  } catch (error) {
    showUploadError(error.message || "Upload failed. Please try again.");
    setProceedEnabled(true);
  }
});
