import Vue from "vue";
import Router from "vue-router";

import VueMeta from "vue-meta";

import NotFoundView from "@/views/NotFoundView";

import analyticsRoutes from "@/modules/analytics/routes";
import breakfastsRoutes from "@/modules/breakfasts/routes";
import calendarRoutes from "@/modules/calendar/routes";
import greenWorkingDaysRoutes from "@/modules/green-working-days/routes";
import holidaysRoutes from "@/modules/holidays/routes";
import notificationsRoutes from "@/modules/notifications/routes";
import scrumRoutes from "@/modules/scrum/routes";
import supportWorkingDaysRoutes from "@/modules/support-working-days/routes";

Vue.use(Router);
Vue.use(VueMeta);

export const routes = [
  {
    path: "/",
    name: "home",
    redirect: { name: "timeline" },
  },

  ...calendarRoutes,
  ...scrumRoutes,
  ...holidaysRoutes,
  ...greenWorkingDaysRoutes,
  ...supportWorkingDaysRoutes,
  ...breakfastsRoutes,
  ...analyticsRoutes,
  ...notificationsRoutes,

  {
    path: "/admin",
    name: "admin",
    beforeEnter() {
      window.open("/admin", "_blank");
    },
  },
  {
    path: "/logout",
    name: "logout",
    beforeEnter() {
      location.href = "/accounts/logout/";
    },
  },
  {
    path: "*",
    name: "not-found",
    component: NotFoundView,
    meta: {
      keepAlive: true,
    },
  },
];

const router = new Router({
  routes,
});

export default router;
