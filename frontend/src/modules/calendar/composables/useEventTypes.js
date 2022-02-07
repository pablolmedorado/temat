import { toRefs } from "@vue/composition-api";

import { useEventStore } from "@/modules/calendar/stores/events";

export default function () {
  // Store
  const eventStore = useEventStore();

  // State
  const { eventTypes, eventTypesMap } = toRefs(eventStore);

  // Lifecycle hooks
  if (!eventTypes.value.length) {
    eventStore.getEventTypes();
  }

  return {
    // State
    eventTypes,
    eventTypesMap,
    // Methods
    getEventTypes: eventStore.getEventTypes,
  };
}
