import { defineStore } from "pinia";
import { keyBy } from "lodash-es";

import NotificationService from "@/modules/notifications/services/notification-service";

export const useNotificationStore = defineStore("notifications", {
  state: () => {
    return {
      unreadCount: 0,
      notificationTargets: [
        { value: "event", text: "Evento", icon: "mdi-calendar-month", route: { name: "event" } },
        { value: "sprint", text: "Sprint", icon: "mdi-run-fast", route: { name: "sprints" } },
        { value: "userstory", text: "Historia de usuario", icon: "mdi-book-account", route: { name: "user-story" } },
        { value: "holiday", text: "Vacaciones", icon: "mdi-beach", route: { name: "user-holidays" } },
        { value: "greenworkingday", text: "Jornada especial", icon: "mdi-briefcase", route: { name: "green-days" } },
        { value: "supportworkingday", text: "Buzón de soporte", icon: "mdi-face-agent", route: { name: "support" } },
      ],
    };
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
  actions: {
    async getUnreadCount() {
      const response = await NotificationService.unreadCount();
      this.unreadCount = response.data.count;
      return this.unreadCount;
    },
  },
});
