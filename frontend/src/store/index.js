import Vue from "vue";
import Vuex from "vuex";

import { DateTime } from "luxon";

import notificationsModule from "./modules/notifications";
import tagsModule from "./modules/tags";
import calendarModule from "./modules/calendar";
import scrumModule from "./modules/scrum";
import usersModule from "./modules/users";
import breakfastsModule from "./modules/breakfasts";

Vue.use(Vuex);

const defaultSnackbarConfig = {
  value: false,
  color: "info",
  multiLine: false,
  timeout: 5000
};

export default new Vuex.Store({
  state: {
    appName: "TeMaT",
    locale: "es",
    tz: "Europe/Madrid",
    currentYear: DateTime.local().year,
    loggedUser: window.djangoUserData || {},
    pendingRequests: 0,
    snackbar: defaultSnackbarConfig,
    konamiCodeActive: false
  },
  getters: {
    loading: state => Boolean(state.pendingRequests),
    yearOptions: state => [state.currentYear - 1, state.currentYear, state.currentYear + 1]
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
    toggleKonamiCode(state) {
      state.konamiCodeActive = !state.konamiCodeActive;
    }
  },
  actions: {
    showSnackbar({ commit }, payload) {
      const snackbarConfig = {
        ...defaultSnackbarConfig,
        ...payload,
        value: true
      };
      commit("setSnackbar", snackbarConfig);
    },
    clearSnackbar({ commit, state }) {
      setTimeout(() => {
        commit("setSnackbar", { ...state.snackbar, message: undefined, value: false });
      }, 1);
    }
  },
  modules: {
    notifications: notificationsModule,
    tags: tagsModule,
    calendar: calendarModule,
    scrum: scrumModule,
    users: usersModule,
    breakfasts: breakfastsModule
  }
});
