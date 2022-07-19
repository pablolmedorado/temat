import BaseService from "@/services/base-service";

import Api from "@/utils/api";
import Urls from "@/utils/reverse";

class HolidayService extends BaseService {
  basename = "work-organization:holiday";

  flatDates(queryParams) {
    const url = Urls[`${this.basename}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  summary(queryParams) {
    const url = Urls[`${this.basename}-summary`]();
    return Api.get(url, { params: queryParams });
  }

  request(dateArray) {
    const url = Urls[`${this.basename}-request`]();
    return Api.post(url, { dates: dateArray });
  }

  cancel(pk) {
    const url = Urls[`${this.basename}-cancel`]({ pk });
    return Api.patch(url);
  }

  changeApprovalStatus(pk, approvalStatus) {
    return Api.patch(this.detailUrl(pk), { approved: approvalStatus });
  }

  userAvailabilityChartData(queryParams) {
    const url = Urls[`${this.basename}-user-availability-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new HolidayService());

export default service;
