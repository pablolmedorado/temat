import BaseService from "../base-service";

export default class IngredientService extends BaseService {
  static baseUrlName = "breakfasts:ingredient";
  static defaultListParams = { ordering: "name" };
}
