import { useMainStore } from "@/stores/main";

import { userHasPermission } from "@/utils/permissions";

export function adminUsersOnly(to, from, next) {
  const mainStore = useMainStore();
  if (mainStore.loggedUser.is_superuser) {
    next();
  } else {
    mainStore.dispatch("showSnackbar", {
      color: "error",
      message: "Ruta disponible sólo para usuarios administradores.",
    });
    next(from.name === null ? { name: "home" } : false);
  }
}

export function usersWithPermissionOnly(permission) {
  return (to, from, next) => {
    if (userHasPermission(permission)) {
      next();
    } else {
      const mainStore = useMainStore();
      mainStore.dispatch("showSnackbar", {
        color: "error",
        message: "Ruta disponible sólo para usuarios con permisos.",
      });
      next(from.name === null ? { name: "home" } : false);
    }
  };
}
