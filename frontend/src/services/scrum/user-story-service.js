import Api from "../api";
import BaseService from "../base-service";

export default class UserStoryService extends BaseService {
  static baseUrlName = "scrum:user-story";

  static validate(pk, queryParams) {
    const url = Urls[`${this.baseUrlName}-validate`]({ pk });
    return Api.patch(url, undefined, { params: queryParams });
  }

  static copy(pk) {
    const url = Urls[`${this.baseUrlName}-copy`]({ pk });
    return Api.post(url);
  }

  static tasksByUserStory(pk, queryParams) {
    const url = Urls["scrum:user-story-tasks-list"]({ user_story: pk });
    return Api.get(url, { params: queryParams });
  }

  static progressByUserStory(pk, queryParams) {
    const url = Urls["scrum:user-story-progress-list"]({ user_story: pk });
    return Api.get(url, { params: queryParams });
  }

  static effortByUserStory(pk, queryParams) {
    const url = Urls["scrum:user-story-effort-list"]({ user_story: pk });
    return Api.get(url, { params: queryParams });
  }

  static typeChartData(queryParams) {
    const url = Urls["scrum:user-story-type-pie-chart"]();
    return Api.get(url, { params: queryParams });
  }

  static effortRoleChartData(queryParams) {
    const url = Urls["scrum:user-story-effort-role-pie-chart"]();
    return Api.get(url, { params: queryParams });
  }

  static userChartData(queryParams) {
    const url = Urls["scrum:user-story-user-chart"]();
    return Api.get(url, { params: queryParams });
  }

  static delayedChartData(queryParams) {
    const url = Urls["scrum:user-story-delayed-pie-chart"]();
    return Api.get(url, { params: queryParams });
  }

  static overworkedChartData(queryParams) {
    const url = Urls["scrum:user-story-overworked-pie-chart"]();
    return Api.get(url, { params: queryParams });
  }
}
