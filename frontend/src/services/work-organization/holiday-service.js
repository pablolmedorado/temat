import Api from "../api";
import BaseService from "../base-service";

class HolidayService extends BaseService {
  baseUrlName = "work-organization:holiday";

  flatDates(queryParams) {
    const url = Urls[`${this.baseUrlName}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  summary(queryParams) {
    const url = Urls[`${this.baseUrlName}-summary`]();
    return Api.get(url, { params: queryParams });
  }

  request(dateArray) {
    const url = Urls[`${this.baseUrlName}-request`]();
    return Api.post(url, { dates: dateArray });
  }

  cancel(pk) {
    const url = Urls[`${this.baseUrlName}-cancel`]({ pk });
    return Api.patch(url);
  }

  changeApprovalStatus(pk, approvalStatus) {
    return Api.patch(this.detailUrl(pk), { approved: approvalStatus });
  }

  userAvailabilityChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-availability-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new HolidayService());

export default service;
