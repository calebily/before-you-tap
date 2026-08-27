const buttons = [...document.querySelectorAll(".choice-button")];
const selection = document.querySelector("#selection");
const imagePanel = document.querySelector("#image-upload-panel");
const audioPanel = document.querySelector("#audio-upload-panel");
const imageTitle = document.querySelector("#image-upload-title");
const audioTitle = document.querySelector("#audio-upload-title");
const chooseImagesAction = document.querySelector("#choose-images");
const imageInput = document.querySelector("#image-input");
const imagePreview = document.querySelector("#image-preview");
const previewList = document.querySelector("#preview-list");
const fileDetails = document.querySelector("#file-details");
const validateButton = document.querySelector("#validate-upload");
const addImageButton = document.querySelector("#add-image");
const clearImagesButton = document.querySelector("#clear-images");
const chooseAudioAction = document.querySelector("#choose-audio");
const audioInput = document.querySelector("#audio-input");
const audioPreview = document.querySelector("#audio-preview");
const audioPlayer = document.querySelector("#audio-player");
const audioFileDetails = document.querySelector("#audio-file-details");
const checkAudioButton = document.querySelector("#check-audio");
const changeAudioButton = document.querySelector("#change-audio");
const uploadStatus = document.querySelector("#upload-status");
const analysisResult = document.querySelector("#analysis-result");
const riskBadge = document.querySelector("#risk-badge");
const resultSummary = document.querySelector("#result-summary");
const warningSection = document.querySelector("#warning-section");
const warningList = document.querySelector("#warning-list");
const uncertaintySection = document.querySelector("#uncertainty-section");
const uncertaintyList = document.querySelector("#uncertainty-list");
const nextStepsList = document.querySelector("#next-steps-list");

const maxImages = 5;
const maxTotalBytes = 20 * 1024 * 1024;
let selectedFiles = [];
let previewUrls = [];
let selectionMode = "replace";
let selectedAudioFile = null;
let audioPreviewUrl = null;

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

function resetResult() {
  analysisResult.hidden = true;
  delete analysisResult.dataset.risk;
  riskBadge.textContent = "";
  resultSummary.textContent = "";
  warningList.replaceChildren();
  uncertaintyList.replaceChildren();
  nextStepsList.replaceChildren();
  warningSection.hidden = true;
  uncertaintySection.hidden = true;
}

function appendTextList(container, items) {
  items.forEach((item) => {
    const listItem = document.createElement("li");
    listItem.textContent = item;
    container.append(listItem);
  });
}

function showResult(payload) {
  const riskCopy = {
    low_concern: { label: "Low concern", state: "low" },
    be_careful: { label: "Be careful", state: "careful" },
    high_risk: { label: "High risk", state: "high" },
  };
  const risk = riskCopy[payload.risk_level] ?? riskCopy.be_careful;

  analysisResult.dataset.risk = risk.state;
  riskBadge.textContent = risk.label;
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
  analysisResult.focus();
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
    chooseAudioAction.hidden = false;
    return;
  }

  audioPreviewUrl = URL.createObjectURL(selectedAudioFile);
  audioPlayer.src = audioPreviewUrl;
  audioFileDetails.textContent = `${selectedAudioFile.name} · ${formatBytes(selectedAudioFile.size)}`;
  chooseAudioAction.hidden = true;
  audioPreview.hidden = false;
  checkAudioButton.focus();
}

function moveImage(fromIndex, toIndex) {
  if (toIndex < 0 || toIndex >= selectedFiles.length) return;
  const [movedFile] = selectedFiles.splice(fromIndex, 1);
  selectedFiles.splice(toIndex, 0, movedFile);
  resetResult();
  renderPreviews();
}

function removeImage(index) {
  selectedFiles.splice(index, 1);
  resetStatus();
  resetResult();
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
    chooseImagesAction.hidden = false;
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
  addImageButton.hidden = selectedFiles.length >= maxImages;
  chooseImagesAction.hidden = true;
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
    imagePanel.hidden = !isImage;
    audioPanel.hidden = isImage;
    resetStatus();
    resetResult();
    (isImage ? imageTitle : audioTitle).focus();
  });
});

chooseImagesAction.addEventListener("click", () => {
  selectionMode = "replace";
});

addImageButton.addEventListener("click", () => {
  selectionMode = "add";
  imageInput.value = "";
  imageInput.click();
});

clearImagesButton.addEventListener("click", () => {
  selectedFiles = [];
  resetStatus();
  resetResult();
  renderPreviews();
  chooseImagesAction.focus();
});

imageInput.addEventListener("change", () => {
  const incomingFiles = [...imageInput.files];
  if (incomingFiles.length === 0) return;

  const candidateFiles =
    selectionMode === "add" ? [...selectedFiles, ...incomingFiles] : incomingFiles;
  if (candidateFiles.length > maxImages) {
    showStatus(`Please choose no more than ${maxImages} images for one check.`, "error");
    imageInput.value = "";
    return;
  }

  const totalBytes = candidateFiles.reduce((sum, file) => sum + file.size, 0);
  if (totalBytes > maxTotalBytes) {
    showStatus("The selected images are over the 20 MB total limit.", "error");
    imageInput.value = "";
    return;
  }

  selectedFiles = candidateFiles;
  resetStatus();
  resetResult();
  renderPreviews();
});

audioInput.addEventListener("change", () => {
  const [file] = audioInput.files;
  if (!file) return;

  if (file.size > maxTotalBytes) {
    showStatus("The selected audio file is over the 20 MB limit.", "error");
    audioInput.value = "";
    return;
  }

  selectedAudioFile = file;
  resetStatus();
  resetResult();
  renderAudioPreview();
});

changeAudioButton.addEventListener("click", () => {
  audioInput.value = "";
  audioInput.click();
});

validateButton.addEventListener("click", async () => {
  if (selectedFiles.length === 0) {
    showStatus("Please choose at least one image first.", "error");
    return;
  }

  validateButton.disabled = true;
  addImageButton.disabled = true;
  clearImagesButton.disabled = true;
  validateButton.textContent = "Checking for warning signs…";
  resetStatus();
  resetResult();
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
    showResult(payload);
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    validateButton.disabled = false;
    addImageButton.disabled = false;
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
  checkAudioButton.textContent = "Checking for warning signs…";
  resetStatus();
  resetResult();
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
    showResult(payload);
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    checkAudioButton.disabled = false;
    changeAudioButton.disabled = false;
    checkAudioButton.textContent = "Check this audio message";
  }
});

window.addEventListener("beforeunload", () => {
  revokePreviewUrls();
  revokeAudioPreviewUrl();
});
