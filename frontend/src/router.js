import Vue from "vue";
import Router from "vue-router";
import VueMeta from "vue-meta";

import calendarRoutes from "@/modules/calendar/routes";
import scrumRoutes from "@/modules/scrum/routes";
import greenWorkingDaysRoutes from "@/modules/green-working-days/routes";
import supportWorkingDaysRoutes from "@/modules/support-working-days/routes";
import holidaysRoutes from "@/modules/holidays/routes";
import breakfastsRoutes from "@/modules/breakfasts/routes";
import notificationsRoutes from "@/modules/notifications/routes";
import analyticsRoutes from "@/modules/analytics/routes";

import NotFound from "@/views/NotFound";

Vue.use(Router);
Vue.use(VueMeta);

const router = new Router({
  routes: [
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
      component: NotFound,
      meta: {
        keepAlive: true,
      },
    },
  ],
});

export default router;
