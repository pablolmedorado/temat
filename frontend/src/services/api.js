import axios from "axios";

import store from "@/store/index";

const axiosConfig = {
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFTOKEN"
};

export const baseApiClient = axios.create(axiosConfig);

const interceptedApiClient = axios.create(axiosConfig);
interceptedApiClient.interceptors.request.use(config => {
  store.commit("addPendingRequest");
  return config;
});
interceptedApiClient.interceptors.response.use(
  response => {
    store.commit("removePendingRequest");
    return response;
  },
  error => {
    store.commit("removePendingRequest");
    return Promise.reject(error);
  }
);

export default interceptedApiClient;
