import BaseModel from "@/models/base-model";

export default class Notification extends BaseModel {
  static contentType = {
    app: "notifications",
    model: "notification",
  };

  static verboseName = "Notificación";
  static verboseNamePlural = "Notificaciones";

  static serviceBasename = "common:notification";

  static localStorageNamespace = "notification";
}
