import Api from "../api";
import BaseService from "../base-service";

class TaskService extends BaseService {
  basename = "scrum:task";

  move(pk, action) {
    return Api.patch(`${this.detailUrl(pk)}${action}/`);
  }

  toggle(pk) {
    const url = Urls[`${this.basename}-toggle`]({ pk });
    return Api.patch(url);
  }
}

const service = Object.freeze(new TaskService());

export default service;
