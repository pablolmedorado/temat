import axios from "axios";
import { get } from "lodash-es";

import { useMainStore } from "@/stores/main";

const axiosConfig = {
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN",
};

const baseApiClient = axios.create(axiosConfig);

baseApiClient.interceptors.request.use((config) => {
  const mainStore = useMainStore();
  mainStore.addPendingRequest();
  return config;
});
baseApiClient.interceptors.response.use(
  (response) => {
    const mainStore = useMainStore();
    mainStore.removePendingRequest();
    return response;
  },
  (error) => {
    const mainStore = useMainStore();
    mainStore.removePendingRequest();
    const code = get(error.response, "status");
    if (code) {
      // eslint-disable-next-line no-console
      console.error(error.response);
      const message = get(error.response, "data.detail", `${error.response.statusText}.`);
      mainStore.showSnackbar({
        color: "error",
        multiLine: true,
        message: `Error ${code}: ${message} Presiona F12 para obtener más detalles.`,
      });
    } else {
      mainStore.showSnackbar({
        color: "error",
        multiLine: true,
        message: "Error de red. Probablemente no tienes conexión a internet o la app está fuera de servicio.",
      });
    }
    return Promise.reject(error);
  }
);

export default baseApiClient;
