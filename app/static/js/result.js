"use strict";

const resultFilename = document.getElementById("result-filename");
const riskScore = document.getElementById("risk-score");
const riskRing = document.getElementById("risk-ring");
const riskLabel = document.getElementById("risk-label");
const summaryMain = document.getElementById("summary-main");
const summarySide = document.getElementById("summary-side");
const redFlagCount = document.getElementById("red-flag-count");
const redFlagsContainer = document.getElementById("red-flags-container");

const rawResult = sessionStorage.getItem("analysis_result");
const filename = sessionStorage.getItem("uploaded_filename") || "Uploaded document";

if (!rawResult) {
  window.location.href = "/upload";
}

function getRiskLabel(score) {
  if (score >= 7.5) {
    return "HIGH EXPOSURE DETECTED";
  }
  if (score >= 4.5) {
    return "MODERATE EXPOSURE";
  }
  return "LOW EXPOSURE";
}

function toRingOffset(score) {
  const radius = 110;
  const circumference = 2 * Math.PI * radius;
  const normalized = Math.max(0, Math.min(10, score)) / 10;
  return `${circumference * (1 - normalized)}`;
}

function renderRedFlags(flags) {
  redFlagsContainer.innerHTML = "";

  if (!flags.length) {
    redFlagsContainer.innerHTML = "<p class='text-secondary'>No explicit red flags were returned by the model.</p>";
    return;
  }

  flags.forEach((flag, index) => {
    const card = document.createElement("div");
    card.className = "group bg-surface-container-low hover:bg-surface-container-lowest transition-all duration-300 p-8 rounded-full flex gap-8 items-start";
    card.innerHTML = `
      <div class="text-error bg-error-container/30 w-12 h-12 shrink-0 rounded-full flex items-center justify-center font-bold text-xl">${index + 1}</div>
      <div class="flex-1">
        <div class="flex justify-between items-center mb-2">
          <h4 class="text-xl font-bold text-primary">Risk Clause ${index + 1}</h4>
          <span class="bg-error-container text-on-error-container text-[10px] px-2 py-0.5 rounded font-bold uppercase tracking-widest">FLAG</span>
        </div>
        <p class="text-on-surface-variant leading-relaxed">${flag}</p>
      </div>
    `;
    redFlagsContainer.appendChild(card);
  });
}

try {
  const parsed = JSON.parse(rawResult);
  const score = Number(parsed.risk_score || 0);
  const flags = Array.isArray(parsed.red_flags) ? parsed.red_flags : [];
  const summary = typeof parsed.summary === "string" ? parsed.summary : "No summary provided.";

  resultFilename.textContent = filename;
  riskScore.textContent = score.toFixed(1);
  riskRing.setAttribute("stroke-dashoffset", toRingOffset(score));
  riskLabel.textContent = getRiskLabel(score);
  summaryMain.textContent = summary;
  summarySide.textContent = summary;
  redFlagCount.textContent = `${flags.length} Issue${flags.length === 1 ? "" : "s"}`;

  renderRedFlags(flags);
} catch (_error) {
  window.location.href = "/upload";
}
