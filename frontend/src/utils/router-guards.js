import store from "@/store/index";

import { userHasPermission } from "@/utils/permissions";

export function adminUsersOnly(to, from, next) {
  if (store.state.loggedUser.is_superuser) {
    next();
  } else {
    store.dispatch("showSnackbar", {
      color: "error",
      message: "Ruta disponible sólo para usuarios administradores.",
    });
    next(false);
  }
}

export function usersWithPermissionOnly(permission) {
  return (to, from, next) => {
    if (userHasPermission(permission)) {
      next();
    } else {
      store.dispatch("showSnackbar", {
        color: "error",
        message: "Ruta disponible sólo para usuarios con permisos.",
      });
      next(false);
    }
  };
}
