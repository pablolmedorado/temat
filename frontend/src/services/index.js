import { get, keyBy } from "lodash-es";

import BreakfastServices from "@/modules/breakfasts/services";
import CalendarServices from "@/modules/calendar/services";
import GreenWorkingDays from "@/modules/green-working-days/services";
import HolidayServices from "@/modules/holidays/services";
import LinkServices from "@/modules/links/services";
import NotificationServices from "@/modules/notifications/services";
import ScrumServices from "@/modules/scrum/services";
import SupportWorkingDays from "@/modules/support-working-days/services";

import GroupService from "./group-service";
import TagService from "./tag-service";
import UserService from "./user-service";

const CommonServices = keyBy([GroupService, TagService, UserService], "basename");

export const serviceCatalog = {
  ...BreakfastServices,
  ...CalendarServices,
  ...CommonServices,
  ...GreenWorkingDays,
  ...HolidayServices,
  ...LinkServices,
  ...NotificationServices,
  ...ScrumServices,
  ...SupportWorkingDays,
};

export function getServiceByBasename(serviceBasename) {
  const service = get(serviceCatalog, serviceBasename);
  if (!service) {
    throw new Error(`Service '${serviceBasename}' not found. Available services: ${Object.keys(serviceCatalog)}.`);
  }
  return service;
}
