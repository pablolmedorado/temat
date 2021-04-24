import BaseService from "../base-service";

class IngredientService extends BaseService {
  baseUrlName = "breakfasts:ingredient";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new IngredientService());

export default service;
