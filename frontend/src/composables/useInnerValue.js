import { getCurrentInstance, ref, watch } from "@vue/composition-api";

export const innerValueProps = {
  value: {
    type: undefined,
    default: undefined,
  },
};

export default function (props) {
  // Vue instance
  const { emit } = getCurrentInstance();

  // State
  const innerValue = ref(props.value);

  // Watchers
  watch(
    () => props.value,
    (newValue) => (innerValue.value = newValue),
    { deep: true }
  );
  watch(innerValue, (newValue) => emit("input", newValue), { deep: true });

  return {
    innerValue,
  };
}
