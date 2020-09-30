import { get, has } from "lodash";

import store from "@/store/index";

export function handleError(error) {
  if (has(error, "response")) {
    handleAPIError(error);
  } else {
    handleUnknownError(error);
  }
}

export function handleAPIError(error) {
  const code = error.response.status;
  const message = get(error, "response.data.detail", `${error.response.statusText}.`);

  // eslint-disable-next-line no-console
  console.error(error.response);
  store.dispatch("showSnackbar", {
    color: "error",
    multiLine: true,
    message: `Error ${code}: ${message} Presiona F12 para obtener más detalles.`
  });
}

export function handleUnknownError() {
  store.dispatch("showSnackbar", {
    color: "error",
    message: "Algo salió mal. Presiona F12 para obtener más detalles."
  });
}
