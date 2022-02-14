import { onMounted, ref } from "@vue/composition-api";

export default function () {
  // State
  const areSupported = ref(undefined);
  const areEnabled = ref(false);

  // Methods
  function handleNotificationPermission(permission) {
    if (!("permission" in Notification)) {
      Notification.permission = permission;
    }
    areEnabled.value = Notification.permission === "granted";
  }

  async function checkNotificationPromise() {
    try {
      await Notification.requestPermission();
      return true;
    } catch {
      return false;
    }
  }

  async function checkNotificationSupport() {
    if (!("Notification" in window)) {
      areSupported.value = false;
      // eslint-disable-next-line no-console
      console.warn("This browser does not support notifications.");
    } else {
      areSupported.value = true;
      if (checkNotificationPromise()) {
        const permission = await Notification.requestPermission();
        handleNotificationPermission(permission);
      } else {
        Notification.requestPermission(function (permission) {
          handleNotificationPermission(permission);
        });
      }
    }
  }

  // Lifecycle hooks
  onMounted(() => {
    checkNotificationSupport();
  });

  return {
    // State
    areSupported,
    areEnabled,
  };
}
