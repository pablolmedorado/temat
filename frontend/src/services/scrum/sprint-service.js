import Api from "../api";
import BaseService from "../base-service";

class SprintService extends BaseService {
  basename = "scrum:sprint";

  burnChartData(pk) {
    const url = Urls[`${this.basename}-burn-chart`]({ pk });
    return Api.get(url);
  }

  ganttChartData(pk) {
    const url = Urls[`${this.basename}-gantt-chart`]({ pk });
    return Api.get(url);
  }

  deploymentReportData(pk) {
    const url = Urls[`${this.basename}-deployment-report`]({ pk });
    return Api.get(url);
  }
}

const service = Object.freeze(new SprintService());

export default service;
