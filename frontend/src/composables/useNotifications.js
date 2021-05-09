import { onMounted, ref } from "@vue/composition-api";

export default function () {
  async function checkNotificationPromise() {
    try {
      await Notification.requestPermission();
      return true;
    } catch {
      return false;
    }
  }

  const areNotificationsEnabled = ref(false);
  function handleNotificationPermission(permission) {
    if (!("permission" in Notification)) {
      Notification.permission = permission;
    }
    areNotificationsEnabled.value = Notification.permission === "granted";
  }

  async function checkNotificationSupport() {
    if (!("Notification" in window)) {
      // eslint-disable-next-line no-console
      console.warn("This browser does not support notifications.");
    } else {
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
    areNotificationsEnabled,
  };
}
