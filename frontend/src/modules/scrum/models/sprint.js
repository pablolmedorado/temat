import { DateTime } from "luxon";

import BaseModel from "@/models/base-model";

export default class Sprint extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "sprint",
  };

  static verboseName = "Sprint";
  static verboseNamePlural = "Sprints";

  static serviceBasename = "scrum:sprint";

  static localStorageNamespace = "sprint";

  static getDefaults = function () {
    return {
      id: null,
      name: "",
      start_date: DateTime.local().toISODate(),
      end_date: null,
      accountable_user: null,
      tags: [],
    };
  };
}
