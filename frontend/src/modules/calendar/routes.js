import TimelineView from "@/modules/calendar/views/TimelineView";
import CalendarView from "@/modules/calendar/views/CalendarView";
import EventListView from "@/modules/calendar/views/events/EventListView";
import EventDetailView from "@/modules/calendar/views/events/EventDetailView";

export default [
  {
    path: "/timeline",
    name: "timeline",
    component: TimelineView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/calendar",
    name: "calendar",
    component: CalendarView,
    props: true,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/calendar/events",
    name: "events",
    component: EventListView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/calendar/events/:id",
    name: "event",
    component: EventDetailView,
    props: true,
    meta: {
      keepAlive: false,
    },
  },
];
