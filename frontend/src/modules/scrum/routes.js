import UserStory from "@/modules/scrum/models/user-story";

import Effort from "@/modules/scrum/views/Effort";
import Epics from "@/modules/scrum/views/Epics";
import SprintChart from "@/modules/scrum/views/sprints/SprintChart";
import SprintDeploymentReport from "@/modules/scrum/views/sprints/SprintDeploymentReport";
import SprintGantt from "@/modules/scrum/views/sprints/SprintGantt";
import SprintKanban from "@/modules/scrum/views/sprints/SprintKanban";
import Sprints from "@/modules/scrum/views/sprints/Sprints";
import UserStories from "@/modules/scrum/views/user-stories/UserStories";
import UserStoryDetail from "@/modules/scrum/views/user-stories/UserStoryDetail";

import { usersWithPermissionOnly } from "@/utils/router-guards";

export default [
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
    beforeEnter: usersWithPermissionOnly(UserStory.ADD_PERMISSION),
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
];
