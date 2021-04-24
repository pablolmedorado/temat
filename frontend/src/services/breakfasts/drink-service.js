import BaseService from "../base-service";

class DrinkService extends BaseService {
  baseUrlName = "breakfasts:drink";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new DrinkService());

export default service;
