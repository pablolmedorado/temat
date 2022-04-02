import { useMainStore } from "@/stores/main";
import { useEventStore } from "@/modules/calendar/stores/events";

export function buildGoogleCalendarUrl(event) {
  const store = useMainStore();
  const eventStore = useEventStore();

  const baseUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&ctz=${store.tz}`;

  const eventType = `[${eventStore.eventTypesMap[event.type].name}] `;

  let dateFormat = "yyyyMMdd'T'HHmm'00'";
  let auxLuxonEnd = event.luxonEnd;
  if (event.all_day) {
    dateFormat = "yyyyMMdd";
    auxLuxonEnd = auxLuxonEnd.plus({ days: 1 });
  }
  const startDateStr = event.luxonStart.toFormat(dateFormat);
  const endDateStr = auxLuxonEnd.toFormat(dateFormat);
  const dates = `${startDateStr}/${endDateStr}`;

  return `${baseUrl}&text=${eventType}${event.name}&dates=${dates}&details=${event.details}&location=${event.location}`;
}
