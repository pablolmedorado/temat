import { computed, getCurrentInstance, ref, watch } from "@vue/composition-api";
import { cloneDeep, difference, forOwn, isArray, isEqualWith, isFunction } from "lodash-es";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import useValidations from "@/composables/useValidations";

export const bulkFormProps = {
  sourceItems: {
    type: Array,
    required: true,
  },
};

export default function (
  props,
  service,
  {
    initializeItem = cloneDeep,
    saveFunctionName = "save",
    buildSaveFunctionArgs,
    successMessage = "Elementos guardados correctamente",
    customErrorMsgs,
  } = {}
) {
  // Vue instance
  const { emit } = getCurrentInstance();

  // Store
  const store = useMainStore();

  // Composables
  const { addTask, removeTask, isTaskLoading } = useLoading();
  const { v$, errorMsgs, getErrorMsgs } = useValidations({ customErrorMsgs });

  // State
  const items = ref(props.sourceItems.map((item) => initializeItem(item)));

  // Computed
  const itemsHaveChanged = computed(() => {
    return !props.sourceItems.every((sourceItem, index) => {
      return isEqualWith(sourceItem, items.value[index], (sourceValue, currentValue) => {
        if (isArray(sourceValue) && isArray(currentValue)) {
          return difference(sourceValue, currentValue).length == 0;
        }
      });
    });
  });
  const isFormLoading = computed(() => isTaskLoading("submit"));

  // Watchers
  watch(
    () => props.sourceItems,
    (newValue) => (items.value = newValue.map((item) => initializeItem(item))),
    { deep: true }
  );
  watch(itemsHaveChanged, (newValue) => emit("changed:items", newValue), { immediate: true });

  // Methods
  function reset() {
    v$.value.$reset();
    items.value = props.sourceItems.map((item) => initializeItem(item));
  }
  async function submit() {
    const valid = await v$.value.$validate();
    if (valid) {
      addTask("submit");
      try {
        const cleanedItems = items.value.map((item) => replaceUndefined(item));
        const args = isFunction(buildSaveFunctionArgs) ? buildSaveFunctionArgs(cleanedItems) : [cleanedItems];
        const response = await service[saveFunctionName](...args);
        store.showSnackbar({
          color: "success",
          message: successMessage,
        });
        return response.data;
      } finally {
        removeTask("submit");
      }
    } else {
      store.showSnackbar({
        color: "error",
        message: "El formulario contiene errores",
      });
      return null;
    }
  }
  function replaceUndefined(item) {
    const newItem = { ...item };
    forOwn(newItem, (value, key, item) => {
      if (value === undefined) {
        item[key] = null;
      }
    });
    return newItem;
  }

  return {
    // Validations
    v$,
    errorMsgs,
    getErrorMsgs,
    // State
    items,
    // Computed
    itemsHaveChanged,
    isFormLoading,
    // Methods
    initializeItem,
    buildSaveFunctionArgs,
    reset,
    submit,
  };
}
