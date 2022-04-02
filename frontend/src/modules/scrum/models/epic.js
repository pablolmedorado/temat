import BaseModel from "@/models/base-model";

export default class Epic extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "epic",
  };

  static verboseName = "Épica";
  static verboseNamePlural = "Épicas";

  static serviceBasename = "scrum:epic";

  static localStorageNamespace = "epic";

  static getDefaults = function () {
    return {
      id: null,
      name: "",
      description: "",
      external_reference: "",
      tags: [],
    };
  };
}
