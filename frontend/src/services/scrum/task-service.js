import Api from "../api";
import BaseService from "../base-service";

export default class TaskService extends BaseService {
  static baseUrlName = "scrum:task";

  static move(pk, action) {
    return Api.patch(`${this.detailUrl(pk)}${action}/`);
  }

  static toggle(pk) {
    const url = Urls[`${this.baseUrlName}-toggle`]({ pk });
    return Api.patch(url);
  }
}
