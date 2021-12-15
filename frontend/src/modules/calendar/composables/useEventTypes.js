import { toRefs } from "@vue/composition-api";

import { useEventStore } from "@/modules/calendar/stores/events";

export default function () {
  const eventStore = useEventStore();
  const { eventTypes, eventTypesMap } = toRefs(eventStore);

  if (!eventTypes.value.length) {
    eventStore.getEventTypes();
  }

  return {
    eventTypes,
    eventTypesMap,
    getEventTypes: eventStore.getEventTypes,
  };
}
