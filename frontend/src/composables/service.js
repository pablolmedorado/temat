import { ref } from "@vue/composition-api";
import { defaultTo, isArray, isFunction, isString } from "lodash-es";

import { useMainStore } from "@/stores/main";

import getService from "@/services";

export function useService(service, fn, options = {}) {
  service = isString(service) ? getService(service) : service;

  // Default options
  const {
    fnArgs = [],
    defaultData,
    successMsg,
    errorMsg = "Ocurrió un error realizando la petición",
    throwErrors = false,
    immediate = false,
  } = options;

  // Store
  const store = useMainStore();

  // State
  const requestLoading = ref(false);
  const requestData = ref(defaultData);
  const requestDataCount = ref(0);

  // Methods
  async function performRequest(...args) {
    requestLoading.value = true;
    try {
      const requestArgs = args.length ? args : fnArgs;
      const response = await service[fn].apply(service, isFunction(requestArgs) ? requestArgs() : [...requestArgs]);

      requestData.value = defaultTo(response.data.results, response.data);
      requestDataCount.value = defaultTo(response.data.count, isArray(response.data) ? response.data.length : 0);

      if (successMsg) {
        store.showSnackbar({
          color: "success",
          message: successMsg,
        });
      }
      return requestData.value;
    } catch (error) {
      requestData.value = null;
      requestDataCount.value = 0;

      if (throwErrors) {
        throw error;
      } else {
        console.error(error);
        store.showSnackbar({
          color: "error",
          message: errorMsg,
        });
        return requestData.value;
      }
    } finally {
      requestLoading.value = false;
    }
  }

  // Initialization
  if (immediate) {
    performRequest();
  }

  return {
    // State
    requestLoading,
    requestData,
    requestDataCount,
    // Methods
    performRequest,
  };
}
