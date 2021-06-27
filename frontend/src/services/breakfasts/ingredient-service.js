import BaseService from "../base-service";

class IngredientService extends BaseService {
  basename = "breakfasts:ingredient";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new IngredientService());

export default service;
