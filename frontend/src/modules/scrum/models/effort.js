import { get, compact } from "lodash-es";
import { DateTime } from "luxon";

import BaseModel from "@/models/base-model";

import { useMainStore } from "@/stores/main";
import { useUserStore } from "@/stores/users";

export default class Effort extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "effort",
  };

  static verboseName = "Esfuerzo";
  static verboseNamePlural = "Esfuerzo";

  static serviceBasename = "scrum:effort";

  static localStorageNamespace = "effort";

  static itemText = function (item) {
    const userStore = useUserStore();
    const representationParts = [
      item.date,
      get(item, "user_story.name"),
      item.user ? get(userStore.userMap, [item.user, "acronym"]) : undefined,
      item.role,
      `${item.effort}UT`,
    ];
    return compact(representationParts).join(" / ");
  };

  static getDefaults = function () {
    const mainStore = useMainStore();
    return {
      id: null,
      date: DateTime.local().toISODate(),
      user: mainStore.currentUser.id,
      role: null,
      user_story: null,
      effort: 1,
      comments: "",
    };
  };
}
