import { ref, onMounted, onUnmounted } from "@vue/composition-api";

export default function (htmlSelector = "body") {
  const isFullscreenEnabled = ref(false);

  function requestFullscreen() {
    const element = document.querySelector(htmlSelector);
    if (element.requestFullscreen) {
      element.requestFullscreen(); // W3C spec
    } else if (element.mozRequestFullScreen) {
      element.mozRequestFullScreen(); // Firefox
    } else if (element.webkitRequestFullscreen) {
      element.webkitRequestFullscreen(); // Safari
    }
  }
  function exitFullscreen() {
    if (document.exitFullscreen) {
      document.exitFullscreen(); // W3C spec
    } else if (document.mozCancelFullScreen) {
      document.mozCancelFullScreen(); // Firefox
    } else if (document.webkitExitFullscreen) {
      document.webkitExitFullscreen(); // Safari
    }
  }
  function toggleFullscreen() {
    if (isFullscreenEnabled.value) {
      exitFullscreen();
    } else {
      requestFullscreen();
    }
  }

  function onFullscreenChange() {
    const fullscreenElement =
      document.fullscreenElement || // W3C spec
      document.mozFullScreenElement || // Firefox
      document.webkitFullscreenElement; // Safari
    isFullscreenEnabled.value = Boolean(fullscreenElement);
  }

  // Lifecycle hooks
  onMounted(() => {
    document.addEventListener("fullscreenchange", onFullscreenChange);
  });
  onUnmounted(() => {
    document.removeEventListener("fullscreenchange", onFullscreenChange);
  });

  return {
    isFullscreenEnabled,
    requestFullscreen,
    exitFullscreen,
    toggleFullscreen,
  };
}
