import BaseService from "@/services/base-service";

class DrinkService extends BaseService {
  basename = "breakfasts:drink";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new DrinkService());

export default service;
