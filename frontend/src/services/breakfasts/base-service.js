import BaseService from "../base-service";

export default class BBaseService extends BaseService {
  static baseUrlName = "breakfasts:base";
  static defaultListParams = { ordering: "name" };
}
