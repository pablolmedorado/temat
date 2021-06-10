import axios from "axios";

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
    return Promise.reject(error);
  }
);

export default baseApiClient;
