import { getCurrentInstance, nextTick, ref, watch } from "@vue/composition-api";

export const dialogProps = {
  value: {
    type: Boolean,
    default: false,
  },
  scrollable: {
    type: Boolean,
    default: true,
  },
  persistent: {
    type: Boolean,
    default: false,
  },
  width: {
    type: [String, Number],
    default: "100%",
  },
  maxWidth: {
    type: [String, Number],
    default: 700,
  },
};

export default function (props) {
  // Vue instance
  const { emit } = getCurrentInstance();

  // State
  const showDialog = ref(props.value);

  // Watchers
  watch(
    () => props.value,
    (newValue) => {
      if (newValue) {
        open();
      } else {
        close();
      }
    }
  );
  watch(showDialog, (newValue) => emit("input", newValue));

  // Methods
  function open() {
    showDialog.value = true;
    return nextTick();
  }
  function close() {
    showDialog.value = false;
    return nextTick();
  }

  return {
    // State
    showDialog,
    // Methods
    open,
    close,
  };
}
