import BaseService from "../base-service";

export default class EventTypeService extends BaseService {
  static baseUrlName = "calendar:event-type";
  static defaultListParams = { ordering: "name" };
}
