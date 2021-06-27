import BaseModel from "@/models/base-model";

export default class SupportWorkingDay extends BaseModel {
  static contentType = {
    app: "work_organization",
    model: "supportworkingday",
  };

  static verboseName = "Jornada de soporte";
  static verboseNamePlural = "Jornadas de soporte";

  static serviceBasename = "work-organization:support";

  static localStorageNamespace = "support";

  static itemText(item) {
    return item.date;
  }
}
