import { keyBy } from "lodash-es";
import { defineStore } from "pinia";

import EventTypeService from "@/modules/calendar/services/event-type-service";

export const useEventStore = defineStore("events", {
  state: () => {
    return {
      eventTypes: [],
      eventVisibilityTypes: [
        { value: "PU", label: "Público", icon: "mdi-earth", colour: "green" },
        { value: "PR", label: "Privado", icon: "mdi-lock", colour: "red" },
      ],
    };
  },
  getters: {
    eventTypesMap: (state) => keyBy(state.eventTypes, "id"),
    eventVisibilityTypesMap: (state) => keyBy(state.eventVisibilityTypes, "value"),
  },
  actions: {
    async getEventTypes() {
      const response = await EventTypeService.list();
      this.eventTypes = response.data;
      return this.eventTypes;
    },
  },
});
