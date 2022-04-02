<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col cols="6">
        <v-select
          v-model.number="item.bread"
          :items="breadOptions"
          item-text="name"
          item-value="id"
          label="Pan*"
          prepend-icon="mdi-baguette"
          :loading="!breadOptions.length"
          :error-messages="getErrorMsgs(v$.item.bread)"
        />
      </v-col>
      <v-col cols="6">
        <v-select
          v-model.number="item.base"
          :items="baseOptions"
          item-text="name"
          item-value="id"
          label="Base*"
          prepend-icon="mdi-soy-sauce"
          :loading="!baseOptions.length"
          :error-messages="getErrorMsgs(v$.item.base)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select
          v-model.number="item.ingredient1"
          :items="ingredientOptions"
          item-text="name"
          item-value="id"
          label="Primer ingrediente"
          prepend-icon="mdi-numeric-1-box"
          :loading="!ingredientOptions.length"
          clearable
          :error-messages="getErrorMsgs(v$.item.ingredient1)"
        />
      </v-col>
      <v-col cols="6">
        <v-select
          v-model.number="item.ingredient2"
          :items="ingredientOptions"
          item-text="name"
          item-value="id"
          label="Segundo ingrediente"
          prepend-icon="mdi-numeric-2-box"
          :loading="!ingredientOptions.length"
          clearable
          :error-messages="getErrorMsgs(v$.item.ingredient2)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-select
          v-model.number="item.drink"
          :items="drinkOptions"
          item-text="name"
          item-value="id"
          label="Bebida"
          prepend-icon="mdi-coffee"
          :loading="!drinkOptions.length"
          clearable
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { toRefs } from "@vue/composition-api";
import { not, required, requiredIf, sameAs } from "@vuelidate/validators";

import BreakfastService from "@/modules/breakfasts/services/breakfast-service";

import { useBreakfastStore } from "@/modules/breakfasts/stores/breakfasts";

import useForm, { formProps } from "@/composables/useForm";

export default {
  name: "BreakfastForm",
  props: formProps,
  validations() {
    return {
      item: {
        bread: { required },
        base: { required },
        ingredient1: { requiredIfIngredient2: requiredIf(this.item.ingredient2) },
        ingredient2: { notSameAsIngredient1: not(sameAs(this.item.ingredient1)) },
      },
    };
  },
  setup(props) {
    // Store
    const breakfastStore = useBreakfastStore();

    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(props, BreakfastService, {
      successMessage: "Desayuno guardado correctamente",
      customErrorMsgs: {
        requiredIfIngredient2: "Requerido si hay ingrediente 2",
        notSameAsIngredient1: "Ingrediente repetido",
      },
    });

    // Computed
    const {
      breads: breadOptions,
      bases: baseOptions,
      ingredients: ingredientOptions,
      drinks: drinkOptions,
    } = toRefs(breakfastStore);

    // Initialization
    if (!breadOptions.length) {
      breakfastStore.getBreads();
    }
    if (!baseOptions.length) {
      breakfastStore.getBases();
    }
    if (!ingredientOptions.length) {
      breakfastStore.getIngredients();
    }
    if (!drinkOptions.length) {
      breakfastStore.getDrinks();
    }

    return {
      // State
      item,
      // Computed
      v$,
      itemHasChanged,
      isFormLoading,
      breadOptions,
      baseOptions,
      ingredientOptions,
      drinkOptions,
      // Methods
      getErrorMsgs,
      submit,
      reset,
    };
  },
};
</script>
