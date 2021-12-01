import HolidayListUserView from "@/modules/holidays/views/HolidayListUserView";
import HolidayTableTeamView from "@/modules/holidays/views/HolidayTableTeamView";

export default [
  {
    path: "/holidays",
    name: "holidays",
    redirect: { name: "user-holidays" },
  },
  {
    path: "/holidays/user",
    name: "user-holidays",
    component: HolidayListUserView,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/holidays/team",
    name: "team-holidays",
    component: HolidayTableTeamView,
    meta: {
      keepAlive: true,
    },
  },
];
