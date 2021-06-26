import BaseModel from "@/models/base-model";

import { DateTime } from "luxon";

export default class Sprint extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "sprint",
  };

  static verboseName = "Sprint";
  static verboseNamePlural = "Sprints";

  static serviceBasename = "scrum:sprint";

  static localStorageNamespace = "sprint";

  static get defaults() {
    return {
      id: null,
      start_date: DateTime.local().toISODate(),
      end_date: null,
      accountable_user: null,
      tags: [],
    };
  }
}
