import BaseModel from "@/models/base-model";

import store from "@/store/index";

export default class Breakfast extends BaseModel {
  static contentType = {
    app: "breakfasts",
    model: "breakfast",
  };

  static verboseName = "Desayuno";
  static verboseNamePlural = "Desayunos";

  static serviceBasename = "breakfasts:breakfast";

  static localStorageNamespace = "breakfast";

  static get defaults() {
    return {
      id: null,
      user: store.state.loggedUser.id,
      bread: null,
      base: null,
      ingredient1: null,
      ingredient2: null,
      drink: null,
    };
  }
}
