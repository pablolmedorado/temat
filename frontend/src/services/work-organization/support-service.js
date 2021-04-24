import Api from "../api";
import BaseService from "../base-service";

class SupportService extends BaseService {
  baseUrlName = "work-organization:support";

  flatDates(queryParams) {
    const url = Urls[`${this.baseUrlName}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  userChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new SupportService());

export default service;
