import UserStory from "@/modules/scrum/models/user-story";

import EffortListView from "@/modules/scrum/views/EffortListView";
import EpicListView from "@/modules/scrum/views/EpicListView";
import SprintBurnChartView from "@/modules/scrum/views/sprints/SprintBurnChartView";
import SprintDeploymentReportView from "@/modules/scrum/views/sprints/SprintDeploymentReportView";
import SprintGanttView from "@/modules/scrum/views/sprints/SprintGanttView";
import SprintKanbanView from "@/modules/scrum/views/sprints/SprintKanbanView";
import SprintListView from "@/modules/scrum/views/sprints/SprintListView";
import UserStoryListView from "@/modules/scrum/views/user-stories/UserStoryListView";
import UserStoryDetailView from "@/modules/scrum/views/user-stories/UserStoryDetailView";

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
    component: SprintListView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/scrum/sprints/:sprintId/kanban",
    name: "sprint-kanban",
    component: SprintKanbanView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/sprints/:sprintId/chart",
    name: "sprint-chart",
    component: SprintBurnChartView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/sprints/:sprintId/gantt",
    name: "sprint-gantt",
    component: SprintGanttView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/sprints/:sprintId/deployment-report",
    name: "sprint-deployment-report",
    component: SprintDeploymentReportView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/sprints/:sprintId/user-stories",
    name: "sprint-user-stories",
    component: UserStoryListView,
    props: true,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/scrum/epics",
    name: "epics",
    component: EpicListView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/scrum/epics/:epicId/user-stories",
    name: "epic-user-stories",
    component: UserStoryListView,
    props: true,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/scrum/user-stories",
    name: "user-stories",
    component: UserStoryListView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/scrum/user-stories/new",
    name: "user-story-new",
    component: UserStoryDetailView,
    beforeEnter: usersWithPermissionOnly(UserStory.ADD_PERMISSION),
    props: (route) => ({ sprintId: route.query.sprint, epicId: route.query.epic }),
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/user-stories/:id",
    name: "user-story",
    component: UserStoryDetailView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/sprints/:sprintId/user-stories/:id",
    name: "sprint-user-story",
    component: UserStoryDetailView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/epics/:epicId/user-stories/:id",
    name: "epic-user-story",
    component: UserStoryDetailView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
  {
    path: "/scrum/effort",
    name: "effort",
    component: EffortListView,
    meta: {
      keepAlive: true,
    },
  },
];
