import Analytics from "@/modules/analytics/views/Analytics";

export default [
  {
    path: "/analytics",
    name: "analytics",
    component: Analytics,
    meta: {
      keepAlive: true,
    },
  },
];
