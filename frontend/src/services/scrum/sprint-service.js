import Api from "../api";
import BaseService from "../base-service";

export default class SprintService extends BaseService {
  static baseUrlName = "scrum:sprint";

  static burnChartData(pk) {
    const url = Urls[`${this.baseUrlName}-burn-chart`]({ pk });
    return Api.get(url);
  }

  static ganttChartData(pk) {
    const url = Urls[`${this.baseUrlName}-gantt-chart`]({ pk });
    return Api.get(url);
  }

  static deploymentReportData(pk) {
    const url = Urls[`${this.baseUrlName}-deployment-report`]({ pk });
    return Api.get(url);
  }
}
