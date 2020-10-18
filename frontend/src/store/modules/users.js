import { keyBy } from "lodash";

import UserService from "@/services/users/user-service";
import GroupService from "@/services/users/group-service";

export default {
  namespaced: true,
  state: {
    users: [],
    groups: [],
  },
  getters: {
    usersWithCompany: (state) => state.users.filter((user) => Boolean(user.company)),
    usersMap: (state) => keyBy(state.users, "id"),
    groupsMap: (state) => keyBy(state.groups, "id"),
  },
  mutations: {
    updateUsers(state, users) {
      state.users = users;
    },
    updateGroups(state, groups) {
      state.groups = groups;
    },
  },
  actions: {
    async getUsers({ commit }) {
      const response = await UserService.list();
      commit("updateUsers", response.data);
      return response.data;
    },
    async getGroups({ commit }) {
      const response = await GroupService.list();
      commit("updateGroups", response.data);
      return response.data;
    },
  },
};
