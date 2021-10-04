<template>
  <v-form v-if="item" ref="itemForm" :disabled="isTaskLoading('submit')">
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
          :error-messages="buildValidationErrorMessages($v.item.bread)"
          @change="$v.item.bread.$touch()"
          @blur="$v.item.bread.$touch()"
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
          :error-messages="buildValidationErrorMessages($v.item.base)"
          @change="$v.item.base.$touch()"
          @blur="$v.item.base.$touch()"
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
          :error-messages="buildValidationErrorMessages($v.item.ingredient1)"
          @change="$v.item.ingredient1.$touch()"
          @blur="$v.item.ingredient1.$touch()"
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
          :error-messages="buildValidationErrorMessages($v.item.ingredient2)"
          @change="$v.item.ingredient2.$touch()"
          @blur="$v.item.ingredient2.$touch()"
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
import { mapActions, mapState } from "vuex";
import { not, required, requiredIf, sameAs } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import BreakfastService from "@/modules/breakfasts/services/breakfast-service";

export default {
  name: "BreakfastForm",
  mixins: [FormMixin({ service: BreakfastService })],
  validations: {
    item: {
      bread: { required },
      base: { required },
      ingredient1: { requiredIfIngredient2: requiredIf("ingredient2") },
      ingredient2: { notSameAsIngredient1: not(sameAs("ingredient1")) },
    },
  },
  data() {
    return {
      successMessage: "Desayuno guardado correctamente",
      validationErrorMessages: {
        requiredIfIngredient2: "Requerido si hay ingrediente 2",
        notSameAsIngredient1: "Ingrediente repetido",
      },
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapState("breakfasts", {
      breadOptions: "breads",
      baseOptions: "bases",
      ingredientOptions: "ingredients",
      drinkOptions: "drinks",
    }),
  },
  created() {
    if (!this.breadOptions.length) {
      this.getBreads();
    }
    if (!this.baseOptions.length) {
      this.getBases();
    }
    if (!this.ingredientOptions.length) {
      this.getIngredients();
    }
    if (!this.drinkOptions.length) {
      this.getDrinks();
    }
  },
  methods: {
    ...mapActions("breakfasts", ["getBreads", "getBases", "getIngredients", "getDrinks"]),
  },
};
</script>
