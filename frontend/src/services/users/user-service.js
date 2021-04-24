import BaseService from "../base-service";

class UserService extends BaseService {
  baseUrlName = "users:user";
  defaultListParams = { ordering: "first_name,last_name,acronym" };
}

const service = Object.freeze(new UserService());

export default service;
