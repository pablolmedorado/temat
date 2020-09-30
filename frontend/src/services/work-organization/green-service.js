import Api from "../api";
import BaseService from "../base-service";

export default class GreenService extends BaseService {
  static baseUrlName = "work-organization:green-day";

  static flatDates(queryParams) {
    const url = Urls[`${this.baseUrlName}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  static toggleVolunteer(pk) {
    const url = Urls[`${this.baseUrlName}-toggle-volunteer`]({ pk });
    return Api.patch(url);
  }

  static userChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-chart`]();
    return Api.get(url, { params: queryParams });
  }
}
