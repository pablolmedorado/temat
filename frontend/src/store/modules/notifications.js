import { keyBy } from "lodash";

import NotificationService from "@/services/notifications/notification-service";

export default {
  namespaced: true,
  state: {
    unreadCount: 0,
    notificationTargets: [
      { value: "event", text: "Evento", icon: "mdi-calendar-month", route: { name: "event" } },
      { value: "sprint", text: "Sprint", icon: "mdi-run-fast", route: { name: "sprints" } },
      { value: "userstory", text: "Historia de usuario", icon: "mdi-book-account", route: { name: "user-story" } },
      { value: "holiday", text: "Vacaciones", icon: "mdi-beach", route: { name: "user-holidays" } },
      { value: "greenworkingday", text: "Jornada especial", icon: "mdi-briefcase", route: { name: "green-days" } },
      { value: "supportworkingday", text: "Buzón de soporte", icon: "mdi-face-agent", route: { name: "support" } },
    ],
  },
  getters: {
    unreadCountBadgeColour(state) {
      if (!state.unreadCount) {
        return "success";
      }
      if (state.unreadCount < 5) {
        return "info";
      }
      if (state.unreadCount < 10) {
        return "warning";
      }
      return "error";
    },
    notificationTargetMap: (state) => keyBy(state.notificationTargets, "value"),
  },
  mutations: {
    setUnreadCount(state, count) {
      state.unreadCount = count;
    },
  },
  actions: {
    async getUnreadCount({ commit }) {
      const response = await NotificationService.unreadCount();
      commit("setUnreadCount", response.data.count);
      return response.data.count;
    },
  },
};
