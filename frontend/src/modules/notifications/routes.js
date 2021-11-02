import NotificationListView from "@/modules/notifications/views/NotificationListView";

export default [
  {
    path: "/notifications",
    name: "notifications",
    component: NotificationListView,
    meta: {
      keepAlive: true,
    },
  },
];
