<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.label"
          label="Etiqueta"
          prepend-icon="mdi-tag"
          counter="100"
          :error-messages="getErrorMsgs(v$.item.label)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <UserAutocomplete
          v-model="item.users"
          label="Usuarios"
          prepend-icon="mdi-account"
          :limit-random-choices-to="item.volunteers"
          show-random-btn
          multiple
          chips
          small-chips
          deletable-chips
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <UserAutocomplete
          v-model="item.volunteers"
          label="Usuarios voluntarios"
          prepend-icon="mdi-account-multiple"
          multiple
          chips
          small-chips
          deletable-chips
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { maxLength, required } from "@vuelidate/validators";

import GreenWorkingDayService from "@/modules/green-working-days/services/green-working-day-service";

import { useForm, formProps } from "@/composables/form";

export default {
  name: "GreenWorkingDayForm",
  props: formProps,
  validations() {
    return {
      item: {
        label: { required, maxLength: maxLength(100) },
      },
    };
  },
  setup() {
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(GreenWorkingDayService, {
      saveFunctionName: "update",
      successMessage: "Jornada especial guardada correctamente",
    });

    return {
      v$,
      getErrorMsgs,
      item,
      itemHasChanged,
      submit,
      reset,
      isFormLoading,
    };
  },
};
</script>
