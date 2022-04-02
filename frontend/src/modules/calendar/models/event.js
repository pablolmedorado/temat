import { DateTime, Interval } from "luxon";

import BaseModel from "@/models/base-model";

export default class CalendarEvent extends BaseModel {
  static contentType = {
    app: "events",
    model: "event",
  };

  static verboseName = "Evento";
  static verboseNamePlural = "Eventos";

  static serviceBasename = "calendar:event";

  static localStorageNamespace = "event";

  static getDefaults = function () {
    const now = DateTime.local().toISO();
    return {
      id: null,
      name: "",
      type: null,
      details: "",
      location: "",
      start_datetime: now,
      end_datetime: now,
      all_day: true,
      visibility: "PU",
      attendees: [],
      groups: [],
      tags: [],
    };
  };

  get luxonStart() {
    return DateTime.fromISO(this.start_datetime);
  }
  get luxonEnd() {
    return DateTime.fromISO(this.end_datetime);
  }
  get luxonInterval() {
    return Interval.fromDateTimes(this.luxonStart, this.luxonEnd);
  }

  get dateFormat() {
    return this.all_day ? "yyyy-MM-dd" : "yyyy-MM-dd HH:mm";
  }
  get start() {
    return this.luxonStart.toFormat(this.dateFormat);
  }
  get end() {
    return this.luxonEnd.toFormat(this.dateFormat);
  }
}
