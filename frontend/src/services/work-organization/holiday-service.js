import Api from "../api";
import BaseService from "../base-service";

export default class HolidayService extends BaseService {
  static baseUrlName = "work-organization:holiday";

  static flatDates(queryParams) {
    const url = Urls[`${this.baseUrlName}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  static summary(queryParams) {
    const url = Urls[`${this.baseUrlName}-summary`]();
    return Api.get(url, { params: queryParams });
  }

  static request(dateArray) {
    const url = Urls[`${this.baseUrlName}-request`]();
    return Api.post(url, { dates: dateArray });
  }

  static cancel(pk) {
    const url = Urls[`${this.baseUrlName}-cancel`]({ pk });
    return Api.patch(url);
  }

  static changeApprovalStatus(pk, approvalStatus) {
    return Api.patch(this.detailUrl(pk), { approved: approvalStatus });
  }

  static userAvailabilityChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-user-availability-chart`]();
    return Api.get(url, { params: queryParams });
  }
}
