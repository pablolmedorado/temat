import { ref, watch } from "@vue/composition-api";
import { isFunction } from "lodash";

export default function (key, initialValue, options = {}) {
  const lsInitialValue = localStorage[key] ? JSON.parse(localStorage[key]) : undefined;
  let value;
  if (lsInitialValue) {
    value = ref(isFunction(options.getter) ? options.getter(lsInitialValue, initialValue) : lsInitialValue);
  } else {
    value = ref(initialValue);
  }

  watch(
    value,
    (newValue) => {
      const lsNewValue = isFunction(options.setter) ? options.setter(newValue, initialValue) : newValue;
      localStorage[key] = JSON.stringify(lsNewValue);
    },
    { deep: true }
  );

  return value;
}
