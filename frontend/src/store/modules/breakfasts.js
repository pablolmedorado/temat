import { keyBy } from "lodash";

import BBaseService from "@/services/breakfasts/base-service";
import BreadService from "@/services/breakfasts/bread-service";
import IngredientService from "@/services/breakfasts/ingredient-service";
import DrinkService from "@/services/breakfasts/drink-service";

export default {
  namespaced: true,
  state: {
    breads: [],
    bases: [],
    ingredients: [],
    drinks: [],
  },
  getters: {
    breadsMap: (state) => keyBy(state.breads, "id"),
    basesMap: (state) => keyBy(state.bases, "id"),
    ingredientsMap: (state) => keyBy(state.ingredients, "id"),
    drinksMap: (state) => keyBy(state.drinks, "id"),
  },
  mutations: {
    setBreads(state, breads) {
      state.breads = breads;
    },
    setBases(state, bases) {
      state.bases = bases;
    },
    setIngredients(state, ingredients) {
      state.ingredients = ingredients;
    },
    setDrinks(state, drinks) {
      state.drinks = drinks;
    },
  },
  actions: {
    async getBreads({ commit }) {
      const response = await BreadService.list();
      commit("setBreads", response.data);
      return response.data;
    },
    async getBases({ commit }) {
      const response = await BBaseService.list();
      commit("setBases", response.data);
      return response.data;
    },
    async getIngredients({ commit }) {
      const response = await IngredientService.list();
      commit("setIngredients", response.data);
      return response.data;
    },
    async getDrinks({ commit }) {
      const response = await DrinkService.list();
      commit("setDrinks", response.data);
      return response.data;
    },
  },
};
