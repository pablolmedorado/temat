import { difference, intersection, memoize } from "lodash";

import store from "@/store/index";

function _userHasPermission(permission) {
  return store.state.loggedUser.is_superuser || store.state.loggedUser.permissions.includes(permission);
}
export const userHasPermission = memoize(_userHasPermission);

function _userHasAllPermissions(permissions) {
  return store.state.loggedUser.is_superuser || !difference(permissions, store.state.loggedUser.permissions).length;
}
export const userHasAllPermissions = memoize(_userHasAllPermissions);

function _userHasAnyPermission(permissions) {
  return (
    store.state.loggedUser.is_superuser || Boolean(intersection(permissions, store.state.loggedUser.permissions).length)
  );
}
export const userHasAnyPermission = memoize(_userHasAnyPermission);
