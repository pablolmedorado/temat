import BaseService from "../base-service";

class GroupService extends BaseService {
  baseUrlName = "users:group";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new GroupService());

export default service;
