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

  static get defaults() {
    return {
      id: null,
      name: "",
      description: "",
      external_reference: "",
      tags: [],
    };
  }
}
