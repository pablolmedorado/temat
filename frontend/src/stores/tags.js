import { defineStore } from "pinia";

import TagService from "@/services/tag-service";

export const useTagStore = defineStore("tags", {
  state: () => {
    return {
      tags: [],
    };
  },
  getters: {
    tagFlatList: (state) => state.tags.map((tag) => tag.name),
  },
  actions: {
    async getTags() {
      const response = await TagService.list();
      this.tags = response.data;
      return this.tags;
    },
  },
});
