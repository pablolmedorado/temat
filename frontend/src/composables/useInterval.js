import { onUnmounted, ref } from "@vue/composition-api";

export default function (callback, delay, { immediate = false }) {
  let intervalId;
  const isActive = ref(false);

  function reset() {
    clearInterval(intervalId);
    intervalId = undefined;
  }
  function start() {
    isActive.value = true;
    reset();
    intervalId = setInterval(callback, delay);
  }
  function stop() {
    isActive.value = false;
    reset();
  }

  // Lifecycle hooks
  onUnmounted(() => {
    clearInterval(intervalId);
  });

  if (immediate) {
    start();
  }

  return {
    isActive,
    start,
    stop,
  };
}
