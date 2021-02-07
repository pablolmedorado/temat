import Vue from "vue";
import Router from "vue-router";
import VueMeta from "vue-meta";

import Timeline from "@/views/calendar/Timeline";
import Calendar from "@/views/calendar/Calendar";
import Events from "@/views/calendar/Events";
import EventDetail from "@/views/calendar/EventDetail";

import Sprints from "@/views/scrum/sprints/Sprints";
import SprintKanban from "@/views/scrum/sprints/SprintKanban";
import SprintChart from "@/views/scrum/sprints/SprintChart";
import SprintGantt from "@/views/scrum/sprints/SprintGantt";
import SprintDeploymentReport from "@/views/scrum/sprints/SprintDeploymentReport";
import UserStories from "@/views/scrum/user-stories/UserStories";
import UserStoryDetail from "@/views/scrum/user-stories/UserStoryDetail";
import Epics from "@/views/scrum/Epics";
import Effort from "@/views/scrum/Effort";

import GreenWorkingDays from "@/views/work-organization/GreenWorkingDays";
import Support from "@/views/work-organization/Support";
import UserHolidays from "@/views/work-organization/holidays/HolidaysUser";
import TeamHolidays from "@/views/work-organization/holidays/HolidaysTeam";

import Breakfasts from "@/views/Breakfasts";
import Analytics from "@/views/Analytics";
import Notifications from "@/views/Notifications";
import NotFound from "@/views/NotFound";

import { adminUsersOnly } from "@/utils/router-guards";

Vue.use(Router);
Vue.use(VueMeta);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "home",
      redirect: { name: "timeline" },
    },

    {
      path: "/timeline",
      name: "timeline",
      component: Timeline,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/calendar",
      name: "calendar",
      component: Calendar,
      props: true,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/calendar/events",
      name: "events",
      component: Events,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/calendar/events/:id",
      name: "event",
      component: EventDetail,
      props: true,
      meta: {
        keepAlive: false,
      },
    },

    {
      path: "/scrum",
      name: "scrum",
      redirect: { name: "sprints" },
    },
    {
      path: "/scrum/sprints",
      name: "sprints",
      component: Sprints,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/scrum/sprints/:sprintId/kanban",
      name: "sprint-kanban",
      component: SprintKanban,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/sprints/:sprintId/chart",
      name: "sprint-chart",
      component: SprintChart,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/sprints/:sprintId/gantt",
      name: "sprint-gantt",
      component: SprintGantt,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/sprints/:sprintId/deployment-report",
      name: "sprint-deployment-report",
      component: SprintDeploymentReport,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/sprints/:sprintId/user-stories",
      name: "sprint-user-stories",
      component: UserStories,
      props: true,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/scrum/epics",
      name: "epics",
      component: Epics,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/scrum/epics/:epicId/user-stories",
      name: "epic-user-stories",
      component: UserStories,
      props: true,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/scrum/user-stories",
      name: "user-stories",
      component: UserStories,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/scrum/user-stories/new",
      name: "user-story-new",
      component: UserStoryDetail,
      beforeEnter: adminUsersOnly,
      props: (route) => ({ sprintId: route.query.sprint, epicId: route.query.epic }),
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/user-stories/:id",
      name: "user-story",
      component: UserStoryDetail,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/sprints/:sprintId/user-stories/:id",
      name: "sprint-user-story",
      component: UserStoryDetail,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/epics/:epicId/user-stories/:id",
      name: "epic-user-story",
      component: UserStoryDetail,
      props: true,
      meta: {
        keepAlive: false,
      },
    },
    {
      path: "/scrum/effort",
      name: "effort",
      component: Effort,
      meta: {
        keepAlive: true,
      },
    },

    {
      path: "/green-days",
      name: "green-days",
      component: GreenWorkingDays,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/support",
      name: "support",
      component: Support,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/holidays",
      name: "holidays",
      redirect: { name: "user-holidays" },
    },
    {
      path: "/holidays/user",
      name: "user-holidays",
      component: UserHolidays,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/holidays/team",
      name: "team-holidays",
      component: TeamHolidays,
      meta: {
        keepAlive: true,
      },
    },

    {
      path: "/breakfasts",
      name: "breakfasts",
      component: Breakfasts,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/analytics",
      name: "analytics",
      component: Analytics,
      meta: {
        keepAlive: true,
      },
    },
    {
      path: "/notifications",
      name: "notifications",
      component: Notifications,
      meta: {
        keepAlive: true,
      },
    },
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
