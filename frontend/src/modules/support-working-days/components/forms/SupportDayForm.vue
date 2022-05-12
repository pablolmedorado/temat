<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <UserAutocomplete
          v-model.number="item.user"
          label="Usuario*"
          prepend-icon="mdi-account"
          show-random-btn
          :error-messages="getErrorMsgs(v$.item.user)"
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { required } from "@vuelidate/validators";

import SupportService from "@/modules/support-working-days/services/support-service";

import { useForm, formProps } from "@/composables/form";

export default {
  name: "SupportDayForm",
  props: formProps,
  validations() {
    return {
      item: {
        user: { required },
      },
    };
  },
  setup() {
    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(SupportService, {
      saveFunctionName: "update",
      successMessage: "Día de soporte guardado correctamente",
    });

    return {
      // State
      item,
      // Computed
      v$,
      itemHasChanged,
      isFormLoading,
      // Methods
      getErrorMsgs,
      submit,
      reset,
    };
  },
};
</script>
