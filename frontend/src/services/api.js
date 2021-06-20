import axios from "axios";
import { get } from "lodash";

import store from "@/store/index";

const axiosConfig = {
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN",
};

const baseApiClient = axios.create(axiosConfig);

baseApiClient.interceptors.request.use((config) => {
  store.commit("addPendingRequest");
  return config;
});
baseApiClient.interceptors.response.use(
  (response) => {
    store.commit("removePendingRequest");
    return response;
  },
  (error) => {
    store.commit("removePendingRequest");
    const code = get(error.response, "status");
    if (code) {
      // eslint-disable-next-line no-console
      console.error(error.response);
      const message = get(error.response, "data.detail", `${error.response.statusText}.`);
      store.dispatch("showSnackbar", {
        color: "error",
        multiLine: true,
        message: `Error ${code}: ${message} Presiona F12 para obtener más detalles.`,
      });
    } else {
      store.dispatch("showSnackbar", {
        color: "error",
        multiLine: true,
        message: "Error de red. Probablemente no tienes conexión a internet o la app está fuera de servicio.",
      });
    }
    return Promise.reject(error);
  }
);

export default baseApiClient;
