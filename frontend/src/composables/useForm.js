import { computed, getCurrentInstance, ref, watch } from "@vue/composition-api";
import { cloneDeep, difference, forOwn, isArray, isEqualWith, isFunction } from "lodash-es";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import useValidations from "@/composables/useValidations";

export const formProps = {
  sourceItem: {
    type: Object,
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
    successMessage = "Elemento guardado correctamente",
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
  const item = ref(initializeItem(props.sourceItem));

  // Computed
  const itemHasChanged = computed(() => {
    return !isEqualWith(props.sourceItem, item.value, (sourceValue, currentValue) => {
      if (isArray(sourceValue) && isArray(currentValue)) {
        return difference(sourceValue, currentValue).length == 0;
      }
    });
  });
  const isFormLoading = computed(() => isTaskLoading("submit"));

  // Watchers
  watch(
    () => props.sourceItem,
    (newValue) => (item.value = initializeItem(newValue))
  );
  watch(itemHasChanged, (newValue) => emit("changed:item", newValue), { immediate: true });

  // Methods
  function reset() {
    item.value = initializeItem(props.sourceItem);
    v$.value.$reset();
  }
  async function submit() {
    const valid = await v$.value.$validate();
    if (valid) {
      addTask("submit");
      try {
        const cleanedItem = replaceUndefined(item.value);
        const args = isFunction(buildSaveFunctionArgs) ? buildSaveFunctionArgs(cleanedItem) : [cleanedItem];
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
    item,
    // Computed
    itemHasChanged,
    isFormLoading,
    // Methods
    initializeItem,
    buildSaveFunctionArgs,
    reset,
    submit,
  };
}
