const STATES = [
  { name: "Idle", color: "#22D3A6" },
  { name: "Listening", color: "#00C2FF" },
  { name: "Thinking", color: "#8B5CF6" },
  { name: "Speaking", color: "#FFB703" }
];

let index = 0;

export function attachJarvisOrb(element, label) {
  function render() {
    const state = STATES[index];
    element.style.setProperty("--orb-color", state.color);
    label.textContent = state.name;
  }

  render();

  element.addEventListener("click", () => {
    index = (index + 1) % STATES.length;
    render();
  });
}