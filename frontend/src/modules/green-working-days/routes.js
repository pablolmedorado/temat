import GreenWorkingDayListView from "@/modules/green-working-days/views/GreenWorkingDayListView";

export default [
  {
    path: "/green-days",
    name: "green-days",
    component: GreenWorkingDayListView,
    meta: {
      keepAlive: true,
    },
  },
];
