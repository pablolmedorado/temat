import HolidayListUserView from "@/modules/holidays/views/HolidayListUserView";
import HolidayListTeamView from "@/modules/holidays/views/HolidayListTeamView";

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
    component: HolidayListTeamView,
    meta: {
      keepAlive: true,
    },
  },
];
