const buttons = [...document.querySelectorAll(".choice-button")];
const selection = document.querySelector("#selection");
const selectionTitle = document.querySelector("#selection-title");

const labels = {
  image: "Image selected",
  audio: "Audio message selected",
};

buttons.forEach((button) => {
  button.setAttribute("aria-pressed", "false");
  button.addEventListener("click", () => {
    buttons.forEach((item) => {
      item.setAttribute("aria-pressed", String(item === button));
    });
    selectionTitle.textContent = labels[button.dataset.kind];
    selection.hidden = false;
  });
});

