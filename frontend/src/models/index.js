import { get } from "lodash";

import BreakfastModels from "./breakfasts";
import CalendarModels from "./calendar";
import CommonModels from "./common";
import ScrumModels from "./scrum";
import UsersModels from "./users";
import WorkOrganizationModels from "./work-organization";

export const modelCatalog = {
  ...BreakfastModels,
  ...CalendarModels,
  ...CommonModels,
  ...ScrumModels,
  ...UsersModels,
  ...WorkOrganizationModels,
};

export default ({ app, model }) => {
  const service = get(modelCatalog, `${app}/${model}`);
  if (!service) {
    throw new Error(`Model '${app}/${model}' not found. Available models: ${Object.keys(modelCatalog)}.`);
  }
  return service;
};
