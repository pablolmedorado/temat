import Vue from "vue";
import Router from "vue-router";

import Timeline from "@/views/calendar/Timeline";
import Calendar from "@/views/calendar/Calendar";
import Events from "@/views/calendar/Events";
import EventDetail from "@/views/calendar/EventDetail";

import Sprints from "@/views/scrum/sprints/Sprints";
import SprintKanban from "@/views/scrum/sprints/SprintKanban";
import SprintChart from "@/views/scrum/sprints/SprintChart";
import SprintGantt from "@/views/scrum/sprints/SprintGantt";
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

Vue.use(Router);

const router = new Router({
  routes: [
    {
      path: "/",
      name: "home",
      redirect: { name: "timeline" }
    },

    {
      path: "/timeline",
      name: "timeline",
      component: Timeline,
      meta: {
        title: "Timeline",
        keepAlive: true
      }
    },
    {
      path: "/calendar",
      name: "calendar",
      component: Calendar,
      meta: {
        title: "Calendario",
        keepAlive: true
      },
      props: true
    },
    {
      path: "/calendar/events",
      name: "events",
      component: Events,
      meta: {
        title: "Eventos",
        keepAlive: true
      }
    },
    {
      path: "/calendar/events/:id",
      name: "event",
      component: EventDetail,
      meta: {
        title: "Evento",
        keepAlive: false
      },
      props: true
    },

    {
      path: "/scrum",
      name: "scrum",
      redirect: { name: "sprints" }
    },
    {
      path: "/scrum/sprints",
      name: "sprints",
      component: Sprints,
      meta: {
        title: "Sprints",
        keepAlive: true
      }
    },
    {
      path: "/scrum/sprints/:sprintId/kanban",
      name: "sprint-kanban",
      component: SprintKanban,
      meta: {
        title: "Sprint - Kanban",
        keepAlive: true
      },
      props: true
    },
    {
      path: "/scrum/sprints/:sprintId/chart",
      name: "sprint-chart",
      component: SprintChart,
      meta: {
        title: "Sprint - Gráfica",
        keepAlive: true
      },
      props: true
    },
    {
      path: "/scrum/sprints/:sprintId/gantt",
      name: "sprint-gantt",
      component: SprintGantt,
      meta: {
        title: "Sprint - Gantt",
        keepAlive: true
      },
      props: true
    },
    {
      path: "/scrum/sprints/:sprintId/user-stories",
      name: "sprint-user-stories",
      component: UserStories,
      meta: {
        title: "Sprint - historias de usuario",
        keepAlive: true
      },
      props: true
    },
    {
      path: "/scrum/epics",
      name: "epics",
      component: Epics,
      meta: {
        title: "Épicas",
        keepAlive: true
      }
    },
    {
      path: "/scrum/epics/:epicId/user-stories",
      name: "epic-user-stories",
      component: UserStories,
      meta: {
        title: "Épica - historias de usuario",
        keepAlive: true
      },
      props: true
    },
    {
      path: "/scrum/user-stories",
      name: "user-stories",
      component: UserStories,
      meta: {
        title: "Índice historias de usuario",
        keepAlive: true
      }
    },
    {
      path: "/scrum/user-stories/new",
      name: "user-story-new",
      component: UserStoryDetail,
      meta: {
        title: "Nueva historia de usuario",
        keepAlive: false
      },
      props: route => ({ sprintId: route.query.sprint, epicId: route.query.epic })
    },
    {
      path: "/scrum/user-stories/:id",
      name: "user-story",
      component: UserStoryDetail,
      props: true,
      meta: {
        title: "Historia de usuario",
        keepAlive: false
      }
    },
    {
      path: "/scrum/sprints/:sprintId/user-stories/:id",
      name: "sprint-user-story",
      component: UserStoryDetail,
      meta: {
        title: "Historia de usuario",
        keepAlive: false
      },
      props: true
    },
    {
      path: "/scrum/epics/:epicId/user-stories/:id",
      name: "epic-user-story",
      component: UserStoryDetail,
      meta: {
        title: "Historia de usuario",
        keepAlive: false
      },
      props: true
    },
    {
      path: "/scrum/effort",
      name: "effort",
      component: Effort,
      meta: {
        title: "Esfuerzo",
        keepAlive: true
      }
    },

    {
      path: "/green-days",
      name: "green-days",
      component: GreenWorkingDays,
      meta: {
        title: "Jornadas especiales",
        keepAlive: true
      }
    },
    {
      path: "/support",
      name: "support",
      component: Support,
      meta: {
        title: "Soporte",
        keepAlive: true
      }
    },
    {
      path: "/holidays",
      name: "holidays",
      redirect: { name: "user-holidays" }
    },
    {
      path: "/holidays/user",
      name: "user-holidays",
      component: UserHolidays,
      meta: {
        title: "Vacaciones usuario",
        keepAlive: true
      }
    },
    {
      path: "/holidays/team",
      name: "team-holidays",
      component: TeamHolidays,
      meta: {
        title: "Vacaciones equipo",
        keepAlive: true
      }
    },

    {
      path: "/breakfasts",
      name: "breakfasts",
      component: Breakfasts,
      meta: {
        title: "Desayunos",
        keepAlive: true
      }
    },
    {
      path: "/analytics",
      name: "analytics",
      component: Analytics,
      meta: {
        title: "Análisis",
        keepAlive: true
      }
    },
    {
      path: "/notifications",
      name: "notifications",
      component: Notifications,
      meta: {
        title: "Notificaciones",
        keepAlive: true
      }
    },
    {
      path: "/admin",
      name: "admin",
      beforeEnter() {
        window.open("/admin", "_blank");
      }
    },
    {
      path: "/logout",
      name: "logout",
      beforeEnter() {
        localStorage.clear();
        if (window.caches) {
          caches.keys().then(cacheNames => {
            cacheNames.forEach(cacheName => {
              caches.delete(cacheName);
            });
          });
        }
        location.href = "/accounts/logout/";
      }
    },
    {
      path: "*",
      name: "NotFound",
      component: NotFound,
      meta: {
        title: "No encontrado",
        keepAlive: true
      }
    }
  ]
});

// https://alligator.io/vuejs/vue-router-modify-head/
// This callback runs before every route change, including on page load.
router.beforeEach((to, from, next) => {
  // This goes through the matched routes from last to first, finding the closest route with a title.
  // eg. if we have /some/deep/nested/route and /some, /deep, and /nested have titles, nested's will be chosen.
  const nearestWithTitle = to.matched
    .slice()
    .reverse()
    .find(r => r.meta && r.meta.title);

  // Find the nearest route element with meta tags.
  const nearestWithMeta = to.matched
    .slice()
    .reverse()
    .find(r => r.meta && r.meta.metaTags);

  // If a route with a title was found, set the document (page) title to that value.
  if (nearestWithTitle) {
    document.title = `${nearestWithTitle.meta.title} | TeMaT`;
  }

  // Remove any stale meta tags from the document using the key attribute we set below.
  Array.from(document.querySelectorAll("[data-vue-router-controlled]")).forEach(el => el.parentNode.removeChild(el));

  // Skip rendering meta tags if there are none.
  if (!nearestWithMeta) {
    next();
  } else {
    // Turn the meta tag definitions into actual elements in the head.
    nearestWithMeta.meta.metaTags
      .map(tagDef => {
        const tag = document.createElement("meta");

        Object.keys(tagDef).forEach(key => {
          tag.setAttribute(key, tagDef[key]);
        });

        // We use this to track which meta tags we create, so we don't interfere with other ones.
        tag.setAttribute("data-vue-router-controlled", "");

        return tag;
      })
      // Add the meta tags to the document head.
      .forEach(tag => document.head.appendChild(tag));

    next();
  }
});

export default router;
