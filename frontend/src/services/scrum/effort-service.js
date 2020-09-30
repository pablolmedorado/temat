import Api from "../api";
import BaseService from "../base-service";

export default class EffortService extends BaseService {
  static baseUrlName = "scrum:effort";

  static roleTimelineChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-role-timeline-chart`]();
    return Api.get(url, { params: queryParams });
  }

  static userTimelineChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-timeline-chart`]();
    return Api.get(url, { params: queryParams });
  }
}
