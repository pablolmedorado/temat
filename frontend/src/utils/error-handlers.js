import { has } from "lodash";

import store from "@/store/index";

function handleUnknownError() {
  store.dispatch("showSnackbar", {
    color: "error",
    message: "Algo salió mal. Presiona F12 para obtener más detalles.",
  });
}

export function handleError(error) {
  if (has(error, "response")) {
    // Error handled by axios
  } else {
    handleUnknownError(error);
  }
}
