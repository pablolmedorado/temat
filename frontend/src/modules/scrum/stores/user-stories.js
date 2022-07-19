import { keyBy } from "lodash-es";
import { defineStore } from "pinia";
import colors from "vuetify/lib/util/colors";

import UserStoryTypeService from "@/modules/scrum/services/user-story-type-service";

export const useUserStoryStore = defineStore("userStory", {
  state: () => {
    return {
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
      cvsVendor: window.djangoData.cvs.vendor,
      cvsBranchBaseUrl: window.djangoData.cvs.branch_base_url,
      cvsIssueBaseUrl: window.djangoData.cvs.issue_base_url,
      cvsPullRequestBaseUrl: window.djangoData.cvs.pull_request_base_url,
    };
  },
  getters: {
    userStoryStatusMap: (state) => keyBy(state.userStoryStatus, "value"),
    userStoryTypesMap: (state) => keyBy(state.userStoryTypes, "id"),
    effortRolesMap: (state) => keyBy(state.effortRoles, "value"),
    riskLevelsMap: (state) => keyBy(state.riskLevels, "value"),
  },
  actions: {
    async getUserStoryTypes() {
      const response = await UserStoryTypeService.list();
      this.userStoryTypes = response.data;
      return this.userStoryTypes;
    },
  },
});
