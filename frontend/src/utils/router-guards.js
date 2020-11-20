import store from "@/store/index";

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
