import BaseService from "../base-service";

class EventTypeService extends BaseService {
  baseUrlName = "calendar:event-type";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new EventTypeService());

export default service;
