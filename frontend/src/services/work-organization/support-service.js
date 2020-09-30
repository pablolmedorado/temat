import Api from "../api";
import BaseService from "../base-service";

export default class SupportService extends BaseService {
  static baseUrlName = "work-organization:support";

  static flatDates(queryParams) {
    const url = Urls[`${this.baseUrlName}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  static userChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-chart`]();
    return Api.get(url, { params: queryParams });
  }
}
