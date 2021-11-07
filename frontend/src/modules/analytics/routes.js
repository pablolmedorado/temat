import AnalyticsView from "@/modules/analytics/views/AnalyticsView";

export default [
  {
    path: "/analytics",
    name: "analytics",
    component: AnalyticsView,
    meta: {
      keepAlive: true,
    },
  },
];
