import Vue from "vue";
import Vuex from "vuex";

import { DateTime } from "luxon";

import breakfastsModule from "@/modules/breakfasts/store";
import calendarModule from "@/modules/calendar/store";
import notificationsModule from "@/modules/notifications/store";
import scrumModule from "@/modules/scrum/store";

import tagsModule from "./modules/tags";
import usersModule from "./modules/users";

import { version } from "@/../package.json";

Vue.use(Vuex);

const defaultSnackbarConfig = {
  value: false,
  color: "info",
  multiLine: false,
  timeout: 5000,
};

export default new Vuex.Store({
  state: {
    appName: "TeMaT",
    locale: "es",
    tz: "Europe/Madrid",
    currentYear: DateTime.local().year,
    loggedUser: { ...window.djangoUserData },
    pendingRequests: 0,
    snackbar: defaultSnackbarConfig,
    isKonamiCodeActive: false,
  },
  getters: {
    appLabel: (state) => ({
      name: state.isKonamiCodeActive ? "MiBeti" : state.appName,
      version: state.isKonamiCodeActive ? "1992" : version,
    }),
    yearOptions: (state) => [state.currentYear - 1, state.currentYear, state.currentYear + 1],
    loadingRequests: (state) => Boolean(state.pendingRequests),
  },
  mutations: {
    addPendingRequest(state) {
      state.pendingRequests += 1;
    },
    removePendingRequest(state) {
      state.pendingRequests -= 1;
    },
    setSnackbar(state, payload) {
      state.snackbar = payload;
    },
    setKonamiCodeActive(state, active) {
      state.isKonamiCodeActive = active;
    },
    toggleKonamiCode(state) {
      state.isKonamiCodeActive = !state.isKonamiCodeActive;
    },
  },
  actions: {
    showSnackbar({ commit }, payload) {
      const snackbarConfig = {
        ...defaultSnackbarConfig,
        ...payload,
        value: true,
      };
      commit("setSnackbar", snackbarConfig);
    },
    clearSnackbar({ commit, state }) {
      setTimeout(() => {
        commit("setSnackbar", { ...state.snackbar, message: undefined, value: false });
      }, 1);
    },
  },
  modules: {
    breakfasts: breakfastsModule,
    calendar: calendarModule,
    notifications: notificationsModule,
    scrum: scrumModule,
    tags: tagsModule,
    users: usersModule,
  },
});
