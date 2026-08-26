const buttons = [...document.querySelectorAll(".choice-button")];
const selection = document.querySelector("#selection");
const imagePanel = document.querySelector("#image-upload-panel");
const audioPanel = document.querySelector("#audio-coming-panel");
const imageTitle = document.querySelector("#image-upload-title");
const audioTitle = document.querySelector("#audio-coming-title");
const imageInput = document.querySelector("#image-input");
const imagePreview = document.querySelector("#image-preview");
const previewImage = document.querySelector("#preview-image");
const fileDetails = document.querySelector("#file-details");
const validateButton = document.querySelector("#validate-upload");
const changeImageButton = document.querySelector("#change-image");
const uploadStatus = document.querySelector("#upload-status");

let selectedFile = null;
let previewUrl = null;

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
    (isImage ? imageTitle : audioTitle).focus();
  });
});

imageInput.addEventListener("change", () => {
  selectedFile = imageInput.files[0] ?? null;
  resetStatus();

  if (previewUrl) {
    URL.revokeObjectURL(previewUrl);
    previewUrl = null;
  }

  if (!selectedFile) {
    imagePreview.hidden = true;
    return;
  }

  previewUrl = URL.createObjectURL(selectedFile);
  previewImage.src = previewUrl;
  fileDetails.textContent = `${selectedFile.name} · ${formatBytes(selectedFile.size)}`;
  imagePreview.hidden = false;
  validateButton.focus();
});

changeImageButton.addEventListener("click", () => imageInput.click());

validateButton.addEventListener("click", async () => {
  if (!selectedFile) {
    showStatus("Please choose an image first.", "error");
    return;
  }

  validateButton.disabled = true;
  validateButton.textContent = "Checking the file…";
  resetStatus();

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch("/api/uploads/validate", {
      method: "POST",
      body: formData,
    });
    const payload = await response.json();

    if (!response.ok) {
      throw new Error(payload.detail || "The image could not be checked.");
    }

    const aiMessage = payload.ai_configured
      ? "The Gemini connection is ready for the next step."
      : "Gemini is not connected yet, so no risk result has been created.";
    showStatus(`${payload.filename} is a supported image. ${aiMessage}`);
  } catch (error) {
    showStatus(error.message, "error");
  } finally {
    validateButton.disabled = false;
    validateButton.textContent = "Check this image";
  }
});

window.addEventListener("beforeunload", () => {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
});
