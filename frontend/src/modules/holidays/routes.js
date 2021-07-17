import UserHolidays from "@/modules/holidays/views/HolidaysUser";
import TeamHolidays from "@/modules/holidays/views/HolidaysTeam";

export default [
  {
    path: "/holidays",
    name: "holidays",
    redirect: { name: "user-holidays" },
  },
  {
    path: "/holidays/user",
    name: "user-holidays",
    component: UserHolidays,
    meta: {
      keepAlive: true,
    },
  },
  {
    path: "/holidays/team",
    name: "team-holidays",
    component: TeamHolidays,
    meta: {
      keepAlive: true,
    },
  },
];
