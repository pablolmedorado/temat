import { difference, intersection, memoize } from "lodash";

import { useMainStore } from "@/stores/main";

function _userHasPermission(permission) {
  const mainStore = useMainStore();
  return mainStore.loggedUser.is_superuser || mainStore.loggedUser.permissions.includes(permission);
}
export const userHasPermission = memoize(_userHasPermission);

function _userHasAllPermissions(permissions) {
  const mainStore = useMainStore();
  return mainStore.loggedUser.is_superuser || !difference(permissions, mainStore.loggedUser.permissions).length;
}
export const userHasAllPermissions = memoize(_userHasAllPermissions);

function _userHasAnyPermission(permissions) {
  const mainStore = useMainStore();
  return (
    mainStore.loggedUser.is_superuser || Boolean(intersection(permissions, mainStore.loggedUser.permissions).length)
  );
}
export const userHasAnyPermission = memoize(_userHasAnyPermission);
