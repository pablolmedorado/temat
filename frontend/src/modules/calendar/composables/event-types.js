import { toRefs } from "@vue/composition-api";

import { useEventStore } from "@/modules/calendar/stores/events";

export function useEventTypes() {
  // Store
  const eventStore = useEventStore();

  // Computed
  const { eventTypes, eventTypesMap } = toRefs(eventStore);

  // Methods
  const getEventTypes = eventStore.getEventTypes;

  // Initialization
  if (!eventStore.eventTypes.length) {
    eventStore.getEventTypes();
  }

  return {
    // Computed
    eventTypes,
    eventTypesMap,
    // Methods
    getEventTypes,
  };
}
