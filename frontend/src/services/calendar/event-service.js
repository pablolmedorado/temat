import { DateTime } from "luxon";

import Api from "../api";
import BaseService from "../base-service";

import CalendarEvent from "@/models/event";

export default class EventService extends BaseService {
  static baseUrlName = "calendar:event";

  static async listCalendar(luxonInterval, excludeSystemEvents) {
    const params = {
      ordering: "start_datetime,name",
      end_datetime__date__gte: luxonInterval.start.toISODate(),
      start_datetime__date__lte: luxonInterval.end.toISODate(),
    };
    if (excludeSystemEvents) {
      params["type__system"] = false;
    }
    const response = await this.list(params);
    return response.data.map((event) => new CalendarEvent(event));
  }

  static myImportantDatesByYear(year) {
    const url = Urls[`${this.baseUrlName}-my-important-dates`]();
    return Api.get(url, { params: { start_datetime__year: year } });
  }

  static myTimeline() {
    const url = Urls[`${this.baseUrlName}-my-events`]();
    return Api.get(url, {
      params: {
        end_datetime__date__gte: DateTime.local().toISODate(),
        ordering: "start_datetime",
        page_size: 10,
      },
    });
  }

  static typeChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-type-pie-chart`]();
    return Api.get(url, {
      params: queryParams,
    });
  }

  static attendeesChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-attendee-packedbubble-chart`]();
    return Api.get(url, {
      params: queryParams,
    });
  }

  static monthlyChartData(queryParams) {
    const url = Urls[`${this.baseUrlName}-monthly-chart`]();
    return Api.get(url, {
      params: queryParams,
    });
  }
}
