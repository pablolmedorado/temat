import Breakfasts from "@/modules/breakfasts/views/Breakfasts";

export default [
  {
    path: "/breakfasts",
    name: "breakfasts",
    component: Breakfasts,
    meta: {
      keepAlive: true,
    },
  },
];
