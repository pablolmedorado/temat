import GreenWorkingDays from "@/modules/green-working-days/views/GreenWorkingDays";

export default [
  {
    path: "/green-days",
    name: "green-days",
    component: GreenWorkingDays,
    meta: {
      keepAlive: true,
    },
  },
];
