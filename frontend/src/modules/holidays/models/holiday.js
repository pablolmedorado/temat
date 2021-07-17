import BaseModel from "@/models/base-model";

export default class Holiday extends BaseModel {
  static contentType = {
    app: "work_organization",
    model: "holiday",
  };
  static serviceBasename = "work-organization:holiday";
}
