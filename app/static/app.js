const buttons = [...document.querySelectorAll(".choice-button")];
const startSection = document.querySelector(".start");
const selection = document.querySelector("#selection");
const listenToggle = document.querySelector("#listen-toggle");
const listenLabel = document.querySelector("#listen-label");
const imagePanel = document.querySelector("#image-upload-panel");
const audioPanel = document.querySelector("#audio-upload-panel");
const imageTitle = document.querySelector("#image-upload-title");
const audioTitle = document.querySelector("#audio-upload-title");
const imageDropZone = document.querySelector("#image-drop-zone");
const chooseImagesAction = document.querySelector("#choose-images");
const imageInput = document.querySelector("#image-input");
const imagePreview = document.querySelector("#image-preview");
const previewList = document.querySelector("#preview-list");
const fileDetails = document.querySelector("#file-details");
const validateButton = document.querySelector("#validate-upload");
const clearImagesButton = document.querySelector("#clear-images");
const audioDropZone = document.querySelector("#audio-drop-zone");
const chooseAudioAction = document.querySelector("#choose-audio");
const audioInput = document.querySelector("#audio-input");
const audioPreview = document.querySelector("#audio-preview");
const audioPlayer = document.querySelector("#audio-player");
const audioFileDetails = document.querySelector("#audio-file-details");
const checkAudioButton = document.querySelector("#check-audio");
const changeAudioButton = document.querySelector("#change-audio");
const removeAudioButton = document.querySelector("#remove-audio");
const uploadStatus = document.querySelector("#upload-status");
const analysisResult = document.querySelector("#analysis-result");
const riskBadge = document.querySelector("#risk-badge");
const resultTitle = document.querySelector("#result-title");
const resultSummary = document.querySelector("#result-summary");
const nextSteps = document.querySelector(".next-steps");
const warningSection = document.querySelector("#warning-section");
const warningList = document.querySelector("#warning-list");
const uncertaintySection = document.querySelector("#uncertainty-section");
const uncertaintyList = document.querySelector("#uncertainty-list");
const nextStepsList = document.querySelector("#next-steps-list");
const fullReportToggle = document.querySelector("#full-report-toggle");
const fullReport = document.querySelector("#full-report");
const hideFullReportButton = document.querySelector("#hide-full-report");

const maxImages = 5;
const maxTotalBytes = 20 * 1024 * 1024;
const supportedImageTypes = new Set(["image/jpeg", "image/png", "image/webp"]);
const supportedImageExtension = /\.(jpe?g|png|webp)$/i;
const supportedAudioTypes = new Set([
  "audio/mpeg",
  "audio/mp3",
  "audio/mp4",
  "audio/m4a",
  "audio/x-m4a",
  "audio/wav",
  "audio/x-wav",
  "audio/ogg",
  "audio/webm",
]);
const supportedAudioExtension = /\.(mp3|m4a|wav|ogg|webm)$/i;
let selectedFiles = [];
let previewUrls = [];
let selectionMode = "replace";
let selectedAudioFile = null;
let audioPreviewUrl = null;
let activeMode = null;
let readAloudEnabled = false;
const resultsByMode = { image: null, audio: null };

function stopSpeaking() {
  if ("speechSynthesis" in window) window.speechSynthesis.cancel();
}

function speakText(text) {
  if (!readAloudEnabled || !("speechSynthesis" in window)) return;
  stopSpeaking();
  const message = new SpeechSynthesisUtterance(text.replace(/\s+/g, " ").trim());
  message.lang = "en-AU";
  message.rate = 0.9;
  window.speechSynthesis.speak(message);
}

function currentReadingText() {
  if (!analysisResult.hidden) {
    if (!fullReport.hidden) return fullReport.innerText;
    return `${riskBadge.innerText}. ${resultTitle.innerText}. ${resultSummary.innerText}. ${nextSteps.innerText}`;
  }

  if (!selection.hidden) {
    const activePanel = activeMode === "image" ? imagePanel : audioPanel;
    return activePanel.innerText;
  }

  return startSection.innerText;
}

if (!("speechSynthesis" in window)) listenToggle.hidden = true;

listenToggle.addEventListener("click", () => {
  readAloudEnabled = !readAloudEnabled;
  listenToggle.setAttribute("aria-pressed", String(readAloudEnabled));
  listenLabel.textContent = readAloudEnabled ? "Listening" : "Listen";
  if (readAloudEnabled) speakText(currentReadingText());
  else stopSpeaking();
});

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} bytes`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function showStatus(message, state = "ready") {
  uploadStatus.textContent = message;
  uploadStatus.dataset.state = state;
  uploadStatus.hidden = false;
}

function resetStatus() {
  uploadStatus.hidden = true;
  uploadStatus.textContent = "";
  delete uploadStatus.dataset.state;
}

function clearRenderedResult() {
  analysisResult.hidden = true;
  delete analysisResult.dataset.risk;
  riskBadge.textContent = "";
  resultTitle.textContent = "";
  resultSummary.textContent = "";
  warningList.replaceChildren();
  uncertaintyList.replaceChildren();
  nextStepsList.replaceChildren();
  warningSection.hidden = true;
  uncertaintySection.hidden = true;
  fullReport.hidden = true;
  fullReportToggle.hidden = false;
  fullReportToggle.setAttribute("aria-expanded", "false");
}

function clearModeResult(mode) {
  resultsByMode[mode] = null;
  if (activeMode === mode) clearRenderedResult();
}

function appendTextList(container, items) {
  items.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    container.append(listItem);
  });
}

function renderResult(payload, { focus = true } = {}) {
  clearRenderedResult();
  const riskCopy = {
    low_concern: {
      label: "Low concern",
      state: "low",
      title: "No strong warning signs found.",
    },
    be_careful: { label: "Be careful", state: "careful", title: "Pause and check first." },
    high_risk: { label: "High risk", state: "high", title: "Stop. Do not act yet." },
  };
  const risk = riskCopy[payload.risk_level] ?? riskCopy.be_careful;

  analysisResult.dataset.risk = risk.state;
  riskBadge.textContent = risk.label;
  resultTitle.textContent = risk.title;
  resultSummary.textContent = payload.summary;

  if (payload.warning_signs.length > 0) {
    payload.warning_signs.forEach((warning) => {
      const card = document.createElement("article");
      card.className = "warning-item";

      const title = document.createElement("h5");
      title.textContent = warning.title;
      const evidence = document.createElement("p");
      evidence.className = "warning-evidence";
      evidence.textContent = warning.evidence;
      const explanation = document.createElement("p");
      explanation.textContent = warning.explanation;

      card.append(title, evidence, explanation);
      warningList.append(card);
    });
    warningSection.hidden = false;
  }

  if (payload.uncertainty.length > 0) {
    appendTextList(uncertaintyList, payload.uncertainty);
    uncertaintySection.hidden = false;
  }

  appendTextList(nextStepsList, payload.safe_next_steps);
  analysisResult.hidden = false;
  if (focus) analysisResult.focus();
  speakText(`${risk.label}. ${risk.title} ${payload.summary}. ${nextSteps.innerText}`);
}

function saveResult(payload, mode) {
  resultsByMode[mode] = payload;
  if (activeMode === mode) renderResult(payload);
}

function revokePreviewUrls() {
  previewUrls.forEach((url) => URL.revokeObjectURL(url));
  previewUrls = [];
}

function revokeAudioPreviewUrl() {
  if (!audioPreviewUrl) return;
  URL.revokeObjectURL(audioPreviewUrl);
  audioPreviewUrl = null;
}

function renderAudioPreview() {
  revokeAudioPreviewUrl();

  if (!selectedAudioFile) {
    audioPlayer.removeAttribute("src");
    audioPlayer.load();
    audioFileDetails.textContent = "";
    audioPreview.hidden = true;
    audioDropZone.hidden = false;
    return;
  }

  audioPreviewUrl = URL.createObjectURL(selectedAudioFile);
  audioPlayer.src = audioPreviewUrl;
  audioFileDetails.textContent = `${selectedAudioFile.name} · ${formatBytes(selectedAudioFile.size)}`;
  audioDropZone.hidden = true;
  audioPreview.hidden = false;
  checkAudioButton.focus();
}

function selectAudioFile(file) {
  const hasSupportedType = supportedAudioTypes.has(file.type);
  const hasSupportedExtension = supportedAudioExtension.test(file.name);
  if (!hasSupportedType && !hasSupportedExtension) {
    showStatus("Please choose an MP3, M4A, WAV, OGG, or WebM audio file.", "error");
    return false;
  }

  if (file.size > maxTotalBytes) {
    showStatus("The selected audio file is over the 20 MB limit.", "error");
    return false;
  }

  selectedAudioFile = file;
  resetStatus();
  clearModeResult("audio");
  renderAudioPreview();
  return true;
}

function selectImageFiles(incomingFiles, mode) {
  if (incomingFiles.length === 0) return false;

  const hasUnsupportedImage = incomingFiles.some((file) => {
    const hasSupportedType = supportedImageTypes.has(file.type);
    const hasSupportedExtension = supportedImageExtension.test(file.name);
    return !hasSupportedType && !hasSupportedExtension;
  });
  if (hasUnsupportedImage) {
    showStatus("Please choose JPEG, PNG, or WebP image files only.", "error");
    return false;
  }

  const candidateFiles = mode === "add" ? [...selectedFiles, ...incomingFiles] : incomingFiles;
  if (candidateFiles.length > maxImages) {
    showStatus(`Please choose no more than ${maxImages} images for one check.`, "error");
    return false;
  }

  const totalBytes = candidateFiles.reduce((sum, file) => sum + file.size, 0);
  if (totalBytes > maxTotalBytes) {
    showStatus("The selected images are over the 20 MB total limit.", "error");
    return false;
  }

  selectedFiles = candidateFiles;
  resetStatus();
  clearModeResult("image");
  renderPreviews();
  return true;
}

function moveImage(fromIndex, toIndex) {
  if (toIndex < 0 || toIndex >= selectedFiles.length) return;
  const [movedFile] = selectedFiles.splice(fromIndex, 1);
  selectedFiles.splice(toIndex, 0, movedFile);
  clearModeResult("image");
  renderPreviews();
}

function removeImage(index) {
  selectedFiles.splice(index, 1);
  resetStatus();
  clearModeResult("image");
  renderPreviews();
}

function createPreviewCard(file, index) {
  const card = document.createElement("article");
  card.className = "preview-card";

  const pageLabel = document.createElement("strong");
  pageLabel.className = "page-label";
  pageLabel.textContent = `Page ${index + 1}`;

  const image = document.createElement("img");
  const previewUrl = URL.createObjectURL(file);
  previewUrls.push(previewUrl);
  image.src = previewUrl;
  image.alt = `Preview of page ${index + 1}`;

  const name = document.createElement("p");
  name.className = "preview-name";
  name.textContent = file.name;

  const controls = document.createElement("div");
  controls.className = "preview-controls";

  const moveEarlier = document.createElement("button");
  moveEarlier.type = "button";
  moveEarlier.textContent = "Move earlier";
  moveEarlier.disabled = index === 0;
  moveEarlier.addEventListener("click", () => moveImage(index, index - 1));

  const moveLater = document.createElement("button");
  moveLater.type = "button";
  moveLater.textContent = "Move later";
  moveLater.disabled = index === selectedFiles.length - 1;
  moveLater.addEventListener("click", () => moveImage(index, index + 1));

  const remove = document.createElement("button");
  remove.type = "button";
  remove.textContent = "Remove";
  remove.addEventListener("click", () => removeImage(index));

  controls.append(moveEarlier, moveLater, remove);
  card.append(pageLabel, image, name, controls);
  return card;
}

function renderPreviews() {
  revokePreviewUrls();
  previewList.replaceChildren();

  if (selectedFiles.length === 0) {
    imagePreview.hidden = true;
    imageInput.value = "";
    return;
  }

  selectedFiles.forEach((file, index) => {
    previewList.append(createPreviewCard(file, index));
  });

  const totalBytes = selectedFiles.reduce((sum, file) => sum + file.size, 0);
  const imageWord = selectedFiles.length === 1 ? "image" : "images";
  fileDetails.textContent = `${selectedFiles.length} ${imageWord} · ${formatBytes(totalBytes)} total`;
  validateButton.textContent =
    selectedFiles.length === 1 ? "Check this image" : "Check these images";
  imagePreview.hidden = false;
  validateButton.focus();
}

buttons.forEach((button) => {
  button.setAttribute("aria-pressed", "false");
  button.addEventListener("click", () => {
    buttons.forEach((item) => {
      item.setAttribute("aria-pressed", String(item === button));
    });
    selection.hidden = false;
    const isImage = button.dataset.kind === "image";
    activeMode = button.dataset.kind;
    imagePanel.hidden = !isImage;
    audioPanel.hidden = isImage;
    resetStatus();
    clearRenderedResult();
    const savedResult = resultsByMode[activeMode];
    if (savedResult) renderResult(savedResult, { focus: false });
    const activeTitle = isImage ? imageTitle : audioTitle;
    activeTitle.focus({ preventScroll: true });
    selection.scrollIntoView({ behavior: "smooth", block: "start" });
    speakText((isImage ? imagePanel : audioPanel).innerText);
  });
});

fullReportToggle.addEventListener("click", () => {
  fullReport.hidden = false;
  fullReportToggle.hidden = true;
  fullReportToggle.setAttribute("aria-expanded", "true");
  fullReport.focus({ preventScroll: true });
  fullReport.scrollIntoView({ behavior: "smooth", block: "start" });
  speakText(fullReport.innerText);
});

hideFullReportButton.addEventListener("click", () => {
  fullReport.hidden = true;
  fullReportToggle.hidden = false;
  fullReportToggle.setAttribute("aria-expanded", "false");
  fullReportToggle.focus({ preventScroll: true });
  analysisResult.scrollIntoView({ behavior: "smooth", block: "start" });
  speakText(`${riskBadge.innerText}. ${resultTitle.innerText}. ${resultSummary.innerText}`);
});

chooseImagesAction.addEventListener("click", () => {
  selectionMode = selectedFiles.length === 0 ? "replace" : "add";
  imageInput.value = "";
  imageInput.click();
});

chooseAudioAction.addEventListener("click", () => {
  audioInput.value = "";
  audioInput.click();
});

clearImagesButton.addEventListener("click", () => {
  selectedFiles = [];
  resetStatus();
  clearModeResult("image");
  renderPreviews();
  imageTitle.focus();
});

imageInput.addEventListener("change", () => {
  const incomingFiles = [...imageInput.files];
  if (incomingFiles.length === 0) return;
  if (!selectImageFiles(incomingFiles, selectionMode)) imageInput.value = "";
});

audioInput.addEventListener("change", () => {
  const [file] = audioInput.files;
  if (!file) return;
  if (!selectAudioFile(file)) audioInput.value = "";
});

function enableDropZone(dropZone, handleFiles) {
  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      event.stopPropagation();
      event.dataTransfer.dropEffect = "copy";
      dropZone.dataset.dragging = "true";
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      event.stopPropagation();
      delete dropZone.dataset.dragging;
    });
  });

  dropZone.addEventListener("drop", (event) => {
    handleFiles([...event.dataTransfer.files]);
  });
}

enableDropZone(imageDropZone, (droppedFiles) => {
  if (droppedFiles.length === 0) {
    showStatus("Please drag one or more image files into this area.", "error");
    return;
  }
  const mode = selectedFiles.length === 0 ? "replace" : "add";
  selectImageFiles(droppedFiles, mode);
});

enableDropZone(audioDropZone, (droppedFiles) => {
  if (droppedFiles.length !== 1) {
    showStatus("Please drag one audio file at a time.", "error");
    return;
  }
  selectAudioFile(droppedFiles[0]);
});

document.addEventListener("paste", (event) => {
  if (activeMode !== "image") return;

  const clipboardItems = event.clipboardData ? [...event.clipboardData.items] : [];
  const pastedImages = clipboardItems
    .filter((item) => item.kind === "file" && item.type.startsWith("image/"))
    .map((item) => item.getAsFile())
    .filter(Boolean);
  if (pastedImages.length === 0) return;

  event.preventDefault();
  const mode = selectedFiles.length === 0 ? "replace" : "add";
  selectImageFiles(pastedImages, mode);
});

changeAudioButton.addEventListener("click", () => {
  audioInput.value = "";
  audioInput.click();
});

removeAudioButton.addEventListener("click", () => {
  selectedAudioFile = null;
  audioInput.value = "";
  resetStatus();
  clearModeResult("audio");
  renderAudioPreview();
});

validateButton.addEventListener("click", async () => {
  if (selectedFiles.length === 0) {
    showStatus("Please choose at least one image first.", "error");
    return;
  }

  validateButton.disabled = true;
  clearImagesButton.disabled = true;
  validateButton.textContent = "Checking for warning signs…";
  resetStatus();
  clearModeResult("image");
  const imageWord = selectedFiles.length === 1 ? "image" : "images";
  showStatus(`Gemini is reviewing ${selectedFiles.length} ${imageWord}. This can take a few seconds.`);

  const formData = new FormData();
  selectedFiles.forEach((file) => formData.append("files", file));

  try {
    const response = await fetch("/api/analyse/images", {
      method: "POST",
      body: formData,
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "The images could not be checked.");
    }

    resetStatus();
    saveResult(payload, "image");
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    validateButton.disabled = false;
    clearImagesButton.disabled = false;
    validateButton.textContent =
      selectedFiles.length === 1 ? "Check this image" : "Check these images";
  }
});

checkAudioButton.addEventListener("click", async () => {
  if (!selectedAudioFile) {
    showStatus("Please choose an audio file first.", "error");
    return;
  }

  checkAudioButton.disabled = true;
  changeAudioButton.disabled = true;
  removeAudioButton.disabled = true;
  checkAudioButton.textContent = "Checking for warning signs…";
  resetStatus();
  clearModeResult("audio");
  showStatus("Gemini is reviewing the saved audio. This can take a few seconds.");

  const formData = new FormData();
  formData.append("file", selectedAudioFile);

  try {
    const response = await fetch("/api/analyse/audio", {
      method: "POST",
      body: formData,
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "The audio message could not be checked.");
    }

    resetStatus();
    saveResult(payload, "audio");
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    checkAudioButton.disabled = false;
    changeAudioButton.disabled = false;
    removeAudioButton.disabled = false;
    checkAudioButton.textContent = "Check this audio message";
  }
});

window.addEventListener("beforeunload", () => {
  revokePreviewUrls();
  revokeAudioPreviewUrl();
});
