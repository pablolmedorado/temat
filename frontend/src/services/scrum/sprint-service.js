import Api from "../api";
import BaseService from "../base-service";

class SprintService extends BaseService {
  baseUrlName = "scrum:sprint";

  burnChartData(pk) {
    const url = Urls[`${this.baseUrlName}-burn-chart`]({ pk });
    return Api.get(url);
  }

  ganttChartData(pk) {
    const url = Urls[`${this.baseUrlName}-gantt-chart`]({ pk });
    return Api.get(url);
  }

  deploymentReportData(pk) {
    const url = Urls[`${this.baseUrlName}-deployment-report`]({ pk });
    return Api.get(url);
  }
}

const service = Object.freeze(new SprintService());

export default service;
