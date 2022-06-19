import BaseService from "@/services/base-service";

import Api from "@/utils/api";
import Urls from "@/utils/reverse";

class EffortService extends BaseService {
  basename = "scrum:effort";

  roleTimelineChartData(queryParams) {
    const url = Urls[`${this.basename}-role-timeline-chart`]();
    return Api.get(url, { params: queryParams });
  }

  userTimelineChartData(queryParams) {
    const url = Urls[`${this.basename}-user-timeline-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new EffortService());

export default service;
