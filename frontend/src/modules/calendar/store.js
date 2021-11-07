import { keyBy } from "lodash";

import EventTypeService from "@/modules/calendar/services/event-type-service";

export default {
  namespaced: true,
  state: {
    eventTypes: [],
    eventVisibilityTypes: [
      { value: "PU", label: "Público", icon: "mdi-earth", colour: "green" },
      { value: "PR", label: "Privado", icon: "mdi-lock", colour: "red" },
    ],
  },
  getters: {
    eventTypesMap: (state) => keyBy(state.eventTypes, "id"),
    eventVisibilityTypesMap: (state) => keyBy(state.eventVisibilityTypes, "value"),
  },
  mutations: {
    setEventTypes(state, eventTypes) {
      state.eventTypes = eventTypes;
    },
  },
  actions: {
    async getEventTypes({ commit }) {
      const response = await EventTypeService.list();
      commit("setEventTypes", response.data);
      return response.data;
    },
  },
};
