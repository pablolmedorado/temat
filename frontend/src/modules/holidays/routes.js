import HolidayUserView from "@/modules/holidays/views/HolidayUserView";
import HolidayTeamView from "@/modules/holidays/views/HolidayTeamView";

export default [
  {
    path: "/holidays",
    name: "holidays",
    redirect: { name: "user-holidays" },
  },
  {
    path: "/holidays/user",
    name: "user-holidays",
    component: HolidayUserView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/holidays/team",
    name: "team-holidays",
    component: HolidayTeamView,
    meta: {
      keepAlive: true,
    },
  },
];
