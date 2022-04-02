import BaseModel from "@/models/base-model";

export default class UserStory extends BaseModel {
  static contentType = {
    app: "scrum",
    model: "userstory",
  };

  static verboseName = "Historia de usuario";
  static verboseNamePlural = "Historias de usuario";

  static serviceBasename = "scrum:user-story";

  static localStorageNamespace = "userStory";

  static getDefaults = function () {
    return {
      id: null,
      name: "",
      type: null,
      epic: null,
      sprint: null,
      functional_description: "",
      technical_description: "",
      external_resource: "",
      start_date: null,
      end_date: null,
      current_progress: 0,
      current_progress_changed: null,
      validated: null,
      validated_changed: null,
      status: 0,
      planned_effort: 1,
      priority: 10,
      development_user: null,
      development_comments: "",
      validation_user: null,
      validation_comments: "",
      support_user: null,
      support_comments: "",
      cvs_reference: "",
      risk_level: 0,
      risk_comments: "",
      use_migrations: false,
      deployment_notes: "",
      tags: [],
    };
  };
}
