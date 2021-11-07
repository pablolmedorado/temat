import SupportListView from "@/modules/support-working-days/views/SupportListView";

export default [
  {
    path: "/support",
    name: "support",
    component: SupportListView,
    meta: {
      keepAlive: true,
    },
  },
];
