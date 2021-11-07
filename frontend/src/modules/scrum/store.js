import colors from "vuetify/lib/util/colors";
import { keyBy } from "lodash";

import UserStoryTypeService from "@/modules/scrum/services/user-story-type-service";

export default {
  namespaced: true,
  state: {
    userStoryStatus: [
      { value: 0, label: "Backlog" },
      { value: 1, label: "Sin comenzar" },
      { value: 2, label: "En desarrollo" },
      { value: 3, label: "En validación" },
      { value: 4, label: "Completada" },
    ],
    userStoryTypes: [],
    effortRoles: [
      { value: "D", label: "Desarrollo", colour: colors.indigo.base },
      { value: "V", label: "Validación", colour: colors.green.base },
      { value: "S", label: "Soporte", colour: colors.grey.base },
    ],
    riskLevels: [
      { value: 0, label: "Verde", icon: "mdi-emoticon-happy", colour: colors.green.base },
      { value: 1, label: "Naranja", icon: "mdi-emoticon-confused", colour: colors.orange.base },
      { value: 2, label: "Rojo", icon: "mdi-emoticon-poop", colour: colors.red.base },
    ],
  },
  getters: {
    userStoryStatusMap: (state) => keyBy(state.userStoryStatus, "value"),
    userStoryTypesMap: (state) => keyBy(state.userStoryTypes, "id"),
    effortRolesMap: (state) => keyBy(state.effortRoles, "value"),
    riskLevelsMap: (state) => keyBy(state.riskLevels, "value"),
  },
  mutations: {
    setUserStoryTypes(state, userStoryTypes) {
      state.userStoryTypes = userStoryTypes;
    },
  },
  actions: {
    async getUserStoryTypes({ commit }) {
      const response = await UserStoryTypeService.list();
      commit("setUserStoryTypes", response.data);
      return response.data;
    },
  },
};
