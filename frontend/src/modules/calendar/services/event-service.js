import { DateTime } from "luxon";

import Api from "@/utils/api";
import BaseService from "@/services/base-service";

import CalendarEvent from "@/modules/calendar/models/event";

class EventService extends BaseService {
  basename = "calendar:event";

  async listCalendar(luxonInterval, excludeSystemEvents) {
    const params = {
      ordering: "start_datetime,name",
      end_datetime__date__gte: luxonInterval.start.toISODate(),
      start_datetime__date__lte: luxonInterval.end.toISODate(),
    };
    if (excludeSystemEvents) {
      params["type__system_slug__isnull"] = true;
    }
    const response = await this.list(params);
    return response.data.map((event) => new CalendarEvent(event));
  }

  myImportantDatesByYear(year) {
    const url = Urls[`${this.basename}-my-important-dates`]();
    return Api.get(url, { params: { start_datetime__year: year } });
  }

  myTimeline() {
    const url = Urls[`${this.basename}-my-events`]();
    return Api.get(url, {
      params: {
        end_datetime__date__gte: DateTime.local().toISODate(),
        ordering: "start_datetime",
        page_size: 10,
      },
    });
  }

  typeChartData(queryParams) {
    const url = Urls[`${this.basename}-type-pie-chart`]();
    return Api.get(url, {
      params: queryParams,
    });
  }

  attendeesChartData(queryParams) {
    const url = Urls[`${this.basename}-attendee-packedbubble-chart`]();
    return Api.get(url, {
      params: queryParams,
    });
  }

  monthlyChartData(queryParams) {
    const url = Urls[`${this.basename}-monthly-chart`]();
    return Api.get(url, {
      params: queryParams,
    });
  }
}

const service = Object.freeze(new EventService());

export default service;
