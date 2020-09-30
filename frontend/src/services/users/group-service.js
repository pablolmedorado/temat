import BaseService from "../base-service";

export default class GroupService extends BaseService {
  static baseUrlName = "users:group";
  static defaultListParams = { ordering: "name" };
}
