import { onBeforeUnmount, onMounted } from "@vue/composition-api";

export default function (callback) {
  const code = [
    "ArrowUp",
    "ArrowUp",
    "ArrowDown",
    "ArrowDown",
    "ArrowLeft",
    "ArrowRight",
    "ArrowLeft",
    "ArrowRight",
    "b",
    "a",
  ];
  const length = code.length;
  let pos = 0;

  function handleKeyDown(event) {
    if (event.key !== undefined) {
      // Handle the event with KeyboardEvent.key and set handled true.
      if (event.key === code[pos]) {
        pos++;
        if (length === pos) {
          callback();
          pos = 0; // ability to start over
        }
      } else {
        pos = 0;
      }
    }
    return false;
  }

  // Lifecycle hooks
  onMounted(() => {
    document.addEventListener("keydown", handleKeyDown, false);
  });
  onBeforeUnmount(() => {
    document.removeEventListener("keydown", handleKeyDown, false);
  });
}
