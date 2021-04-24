import Api from "../api";
import BaseService from "../base-service";

class EffortService extends BaseService {
  baseUrlName = "scrum:effort";

  roleTimelineChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-role-timeline-chart`]();
    return Api.get(url, { params: queryParams });
  }

  userTimelineChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-timeline-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new EffortService());

export default service;
