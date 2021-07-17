import BaseModel from "@/models/base-model";

export default class Task extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "task",
  };

  static verboseName = "Tarea";
  static verboseNamePlural = "Tareas";

  static serviceBasename = "scrum:task";

  static localStorageNamespace = "task";

  static itemText(item) {
    return item.name;
  }

  static get defaults() {
    return { id: null, user_story: null, name: "", weight: 1, done: false };
  }
}
