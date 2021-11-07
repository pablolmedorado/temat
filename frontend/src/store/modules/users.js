import { keyBy } from "lodash";

import UserService from "@/services/user-service";
import GroupService from "@/services/group-service";

export default {
  namespaced: true,
  state: {
    users: [],
    groups: [],
  },
  getters: {
    workerUsers: (state) => state.users.filter((user) => user.is_active && Boolean(user.company)),
    usersMap: (state) => keyBy(state.users, "id"),
    groupsMap: (state) => keyBy(state.groups, "id"),
  },
  mutations: {
    setUsers(state, users) {
      state.users = users;
    },
    setGroups(state, groups) {
      state.groups = groups;
    },
  },
  actions: {
    async getUsers({ commit }) {
      const response = await UserService.list();
      commit("setUsers", response.data);
      return response.data;
    },
    async getGroups({ commit }) {
      const response = await GroupService.list();
      commit("setGroups", response.data);
      return response.data;
    },
  },
};
