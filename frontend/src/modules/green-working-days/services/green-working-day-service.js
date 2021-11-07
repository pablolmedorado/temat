import Api from "@/utils/api";
import BaseService from "@/services/base-service";

class GreenWorkingDayService extends BaseService {
  basename = "work-organization:green-day";

  flatDates(queryParams) {
    const url = Urls[`${this.basename}-flat-dates`]();
    return Api.get(url, { params: queryParams });
  }

  toggleVolunteer(pk) {
    const url = Urls[`${this.basename}-toggle-volunteer`]({ pk });
    return Api.patch(url);
  }

  userChartData(queryParams) {
    const url = Urls[`${this.basename}-user-chart`]();
    return Api.get(url, { params: queryParams });
  }
}

const service = Object.freeze(new GreenWorkingDayService());

export default service;
