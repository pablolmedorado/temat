import { createNamespacedHelpers } from "vuex-composition-helpers";

const { useActions, useGetters, useState } = createNamespacedHelpers("calendar");

export default function () {
  const { eventTypes } = useState(["eventTypes"]);
  const { eventTypesMap } = useGetters(["eventTypesMap"]);
  const { getEventTypes } = useActions(["getEventTypes"]);

  if (!eventTypes.value.length) {
    getEventTypes();
  }

  return {
    eventTypes,
    eventTypesMap,
    getEventTypes,
  };
}
