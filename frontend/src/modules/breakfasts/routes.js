import BreakfastsView from "@/modules/breakfasts/views/BreakfastsView";

export default [
  {
    path: "/breakfasts",
    name: "breakfasts",
    component: BreakfastsView,
    meta: {
      keepAlive: true,
    },
  },
];
