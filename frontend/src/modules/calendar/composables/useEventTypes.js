import { toRefs } from "@vue/composition-api";

import { useEventStore } from "@/modules/calendar/stores/events";

export default function () {
  // Store
  const eventStore = useEventStore();

  // Computed
  const { eventTypes, eventTypesMap } = toRefs(eventStore);

  // Initialization
  if (!eventStore.eventTypes.length) {
    eventStore.getEventTypes();
  }

  return {
    // Computed
    eventTypes,
    eventTypesMap,
    // Methods
    getEventTypes: eventStore.getEventTypes,
  };
}
