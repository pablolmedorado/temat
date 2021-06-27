import { get, compact } from "lodash";
import { DateTime } from "luxon";

import BaseModel from "@/models/base-model";

import store from "@/store/index";

export default class Effort extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "effort",
  };

  static verboseName = "Esfuerzo";
  static verboseNamePlural = "Esfuerzo";

  static serviceBasename = "scrum:effort";

  static localStorageNamespace = "effort";

  static itemText(item) {
    const usersMap = store.getters["users/usersMap"];
    const representationParts = [
      item.date,
      get(item, "user_story.name"),
      item.user ? get(usersMap, [item.user, "acronym"]) : undefined,
      item.role,
      `${item.effort}UT`,
    ];
    return compact(representationParts).join(" / ");
  }

  static get defaults() {
    return {
      id: null,
      date: DateTime.local().toISODate(),
      user: store.state.loggedUser.id,
      role: null,
      user_story: null,
      effort: 1,
      comments: "",
    };
  }
}
