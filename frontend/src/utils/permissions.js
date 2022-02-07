import { difference, intersection, memoize } from "lodash";

import { useMainStore } from "@/stores/main";

function _userHasPermission(permission) {
  const mainStore = useMainStore();
  return mainStore.currentUser.is_superuser || mainStore.currentUser.permissions.includes(permission);
}
export const userHasPermission = memoize(_userHasPermission);

function _userHasAllPermissions(permissions) {
  const mainStore = useMainStore();
  return mainStore.currentUser.is_superuser || !difference(permissions, mainStore.currentUser.permissions).length;
}
export const userHasAllPermissions = memoize(_userHasAllPermissions);

function _userHasAnyPermission(permissions) {
  const mainStore = useMainStore();
  return (
    mainStore.currentUser.is_superuser || Boolean(intersection(permissions, mainStore.currentUser.permissions).length)
  );
}
export const userHasAnyPermission = memoize(_userHasAnyPermission);
