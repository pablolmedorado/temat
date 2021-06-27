import { get } from "lodash";

import BreakfastServices from "./breakfasts";
import CalendarServices from "./calendar";
import CommonServices from "./common";
import ScrumServices from "./scrum";
import UsersServices from "./users";
import WorkOrganizationServices from "./work-organization";

export const serviceCatalog = {
  ...BreakfastServices,
  ...CalendarServices,
  ...CommonServices,
  ...ScrumServices,
  ...UsersServices,
  ...WorkOrganizationServices,
};

export default (serviceBasename) => {
  const service = get(serviceCatalog, serviceBasename);
  if (!service) {
    throw new Error(`Service '${serviceBasename}' not found. Available services: ${Object.keys(serviceCatalog)}.`);
  }
  return service;
};
