import BaseService from "../base-service";

export default class UserService extends BaseService {
  static baseUrlName = "users:user";
  static defaultListParams = { ordering: "first_name,last_name,acronym" };
}
