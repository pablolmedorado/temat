import { DateTime, Duration } from "luxon";

import store from "@/store/index";

export function isoDateToLocaleString(isoDate, format) {
  if (!isoDate) {
    return null;
  }
  const locale = store.state.locale;
  return DateTime.fromISO(isoDate)
    .setLocale(locale)
    .toLocaleString(format || DateTime.DATE_HUGE);
}

export function isoDateTimeToLocaleString(isoDateTime, format) {
  if (!isoDateTime) {
    return null;
  }
  const locale = store.state.locale;
  return DateTime.fromISO(isoDateTime)
    .setLocale(locale)
    .toLocaleString(format || DateTime.DATETIME_MED_WITH_SECONDS);
}

export function getReadableDuration(durationObj) {
  const duration = Duration.fromObject(durationObj)
    .shiftTo("days", "hours", "minutes", "seconds")
    .toObject();
  let result = "";
  if (duration.days) {
    result += `${duration.days} ${duration.days === 1 ? "día" : "días"}`;
  }
  if (duration.days && duration.hours) {
    result += `, `;
  }
  if (duration.hours) {
    result += `${duration.hours} ${duration.hours === 1 ? "hora" : "horas"}`;
  }
  if ((duration.days || duration.hours) && duration.minutes) {
    result += ` y `;
  }
  if (duration.minutes) {
    result += `${duration.minutes} ${duration.minutes === 1 ? "minuto" : "minutos"}`;
  }
  return result;
}
