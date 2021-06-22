import Api from "../api";
import BaseService from "../base-service";

class SupportService extends BaseService {
  basename = "work-organization:support";

  flatDates(queryParams) {
    const url = Urls[`${this.basename}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  userChartData(queryParams) {
    const url = Urls[`${this.basename}-user-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new SupportService());

export default service;
