import Timeline from "@/modules/calendar/views/Timeline";
import Calendar from "@/modules/calendar/views/Calendar";
import Events from "@/modules/calendar/views/events/Events";
import EventDetail from "@/modules/calendar/views/events/EventDetail";

export default [
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
];
