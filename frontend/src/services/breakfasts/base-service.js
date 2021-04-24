import BaseService from "../base-service";

class BBaseService extends BaseService {
  baseUrlName = "breakfasts:base";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new BBaseService());

export default service;
