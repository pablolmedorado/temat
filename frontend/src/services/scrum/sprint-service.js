import Api from "../api";
import BaseService from "../base-service";

export default class SprintService extends BaseService {
  static baseUrlName = "scrum:sprint";

  static burnChartData(pk) {
    const url = Urls[`${this.baseUrlName}-burn-chart`]({ pk });
    return Api.get(url);
  }
}
