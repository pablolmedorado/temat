import BaseService from "../base-service";

export default class DrinkService extends BaseService {
  static baseUrlName = "breakfasts:drink";
  static defaultListParams = { ordering: "name" };
}
