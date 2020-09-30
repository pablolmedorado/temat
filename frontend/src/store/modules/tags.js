import TagService from "@/services/tags/tag-service";

export default {
  namespaced: true,
  state: {
    tags: []
  },
  getters: {
    tagFlatList: state => state.tags.map(tag => tag.name)
  },
  mutations: {
    setTags(state, tags) {
      state.tags = tags;
    }
  },
  actions: {
    async getTags({ commit }) {
      const response = await TagService.list();
      commit("setTags", response.data);
      return response.data;
    }
  }
};
