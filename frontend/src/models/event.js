import { DateTime, Interval } from "luxon";

export default class CalendarEvent {
  static get defaults() {
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
      tags: []
    };
  }

  constructor(data) {
    Object.assign(this, this.constructor.defaults, data);
  }

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
