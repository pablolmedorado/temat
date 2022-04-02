import { has } from "lodash-es";

import { useMainStore } from "@/stores/main";

function handleUnknownError() {
  const mainStore = useMainStore();
  mainStore.showSnackbar({
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
