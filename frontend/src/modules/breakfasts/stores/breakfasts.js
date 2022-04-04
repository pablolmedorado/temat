import { defineStore } from "pinia";
import { keyBy } from "lodash-es";

import BBaseService from "@/modules/breakfasts/services/base-service";
import BreadService from "@/modules/breakfasts/services/bread-service";
import IngredientService from "@/modules/breakfasts/services/ingredient-service";
import DrinkService from "@/modules/breakfasts/services/drink-service";

export const useBreakfastStore = defineStore("breakfasts", {
  state: () => {
    return {
      breads: [],
      bases: [],
      ingredients: [],
      drinks: [],
    };
  },
  getters: {
    breadsMap: (state) => keyBy(state.breads, "id"),
    basesMap: (state) => keyBy(state.bases, "id"),
    ingredientsMap: (state) => keyBy(state.ingredients, "id"),
    drinksMap: (state) => keyBy(state.drinks, "id"),
  },
  actions: {
    async getBreads() {
      const response = await BreadService.list();
      this.breads = response.data;
      return this.breads;
    },
    async getBases() {
      const response = await BBaseService.list();
      this.bases = response.data;
      return this.bases;
    },
    async getIngredients() {
      const response = await IngredientService.list();
      this.ingredients = response.data;
      return this.ingredients;
    },
    async getDrinks() {
      const response = await DrinkService.list();
      this.drinks = response.data;
      return this.drinks;
    },
  },
});
