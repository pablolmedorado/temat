import BaseModel from "@/models/base-model";

export default class GreenWorkingDay extends BaseModel {
  static contentType = {
    app: "work_organization",
    model: "greenworkingday",
  };

  static verboseName = "Jornada especial";
  static verboseNamePlural = "Jornadas especiales";

  static serviceBasename = "work-organization:green-day";

  static localStorageNamespace = "greenWorkingDay";

  static itemText(item) {
    return item.date;
  }
}
