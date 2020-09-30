import BaseService from "../base-service";

export default class BreadService extends BaseService {
  static baseUrlName = "breakfasts:bread";
  static defaultListParams = { ordering: "name" };
}
