import { keyBy } from "lodash-es";
import { defineStore } from "pinia";

import GroupService from "@/services/group-service";
import UserService from "@/services/user-service";

export const useUserStore = defineStore("users", {
  state: () => {
    return {
      users: [],
      groups: [],
    };
  },
  getters: {
    workerUsers: (state) => state.users.filter((user) => user.is_active && Boolean(user.company)),
    userMap: (state) => keyBy(state.users, "id"),
    groupMap: (state) => keyBy(state.groups, "id"),
  },
  actions: {
    async getUsers() {
      const response = await UserService.list();
      this.users = response.data;
      return this.users;
    },
    async getGroups() {
      const response = await GroupService.list();
      this.groups = response.data;
      return this.groups;
    },
  },
});
