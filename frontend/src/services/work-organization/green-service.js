import Api from "../api";
import BaseService from "../base-service";

class GreenService extends BaseService {
  baseUrlName = "work-organization:green-day";

  flatDates(queryParams) {
    const url = Urls[`${this.baseUrlName}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  toggleVolunteer(pk) {
    const url = Urls[`${this.baseUrlName}-toggle-volunteer`]({ pk });
    return Api.patch(url);
  }

  userChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new GreenService());

export default service;
