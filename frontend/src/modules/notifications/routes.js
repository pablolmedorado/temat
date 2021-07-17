import Notifications from "@/modules/notifications/views/Notifications";

export default [
  {
    path: "/notifications",
    name: "notifications",
    component: Notifications,
    meta: {
      keepAlive: true,
    },
  },
];
