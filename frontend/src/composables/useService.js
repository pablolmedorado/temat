import { ref } from "@vue/composition-api";
import { defaultTo, get, isArray, isFunction, isString } from "lodash-es";

import { useMainStore } from "@/stores/main";

import getService from "@/services";

export default function (service, fn, options = {}) {
  service = isString(service) ? getService(service) : service;

  // Store
  const store = useMainStore();

  // State
  const requestLoading = ref(false);
  const requestData = ref(options.defaultData);
  const requestDataCount = ref(0);

  // Methods
  async function performRequest(...args) {
    requestLoading.value = true;
    try {
      const requestArgs = args.length ? args : get(options, "fnArgs", []);
      const response = await service[fn].apply(service, isFunction(requestArgs) ? requestArgs() : [...requestArgs]);

      requestData.value = defaultTo(response.data.results, response.data);
      requestDataCount.value = defaultTo(response.data.count, isArray(response.data) ? response.data.length : 0);

      if (options.successMsg) {
        store.showSnackbar({
          color: "success",
          message: options.successMsg,
        });
      }
      return requestData.value;
    } catch (error) {
      requestData.value = null;
      requestDataCount.value = 0;

      if (options.throwErrors) {
        throw error;
      } else {
        console.error(error);
        store.showSnackbar({
          color: "error",
          message: get(options, "errorMsg", "Ocurrió un error realizando la petición"),
        });
        return requestData.value;
      }
    } finally {
      requestLoading.value = false;
    }
  }

  // Initialization
  if (options.immediate) {
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
