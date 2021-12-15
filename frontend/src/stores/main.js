import { defineStore } from "pinia";

import { DateTime } from "luxon";

import { version } from "@/../package.json";

const defaultSnackbarConfig = {
  value: false,
  color: "info",
  multiLine: false,
  timeout: 5000,
};

export const useMainStore = defineStore("main", {
  state: () => {
    return {
      appName: "TeMaT",
      locale: "es",
      tz: "Europe/Madrid",
      currentYear: DateTime.local().year,
      loggedUser: { ...window.djangoUserData },
      pendingRequests: 0,
      snackbar: defaultSnackbarConfig,
      isKonamiCodeActive: false,
    };
  },
  getters: {
    appLabel: (state) => ({
      name: state.isKonamiCodeActive ? "MiBeti" : state.appName,
      version: state.isKonamiCodeActive ? "1992" : version,
    }),
    yearOptions: (state) => [state.currentYear - 1, state.currentYear, state.currentYear + 1],
    loadingRequests: (state) => Boolean(state.pendingRequests),
  },
  actions: {
    addPendingRequest() {
      this.pendingRequests += 1;
    },
    removePendingRequest() {
      this.pendingRequests -= 1;
    },
    showSnackbar(config) {
      this.snackbar = {
        ...defaultSnackbarConfig,
        ...config,
        value: true,
      };
    },
    clearSnackbar() {
      setTimeout(() => {
        this.snackbar = { ...this.snackbar, message: undefined, value: false };
      }, 1);
    },
    toggleKonamiCode() {
      this.isKonamiCodeActive = !this.isKonamiCodeActive;
    },
  },
});
