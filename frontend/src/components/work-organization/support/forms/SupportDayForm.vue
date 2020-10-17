<template>
  <form v-if="item" ref="itemForm">
    <v-container>
      <v-row>
        <v-col>
          <UserAutocomplete
            v-model.number="item.user"
            label="Usuario*"
            prepend-icon="mdi-account"
            show-random-btn
            :error-messages="buildValidationErrorMessages($v.item.user)"
            @input="$v.item.user.$touch()"
            @blur="$v.item.user.$touch()"
          />
        </v-col>
      </v-row>
      <small>* indica campo obligatorio</small>
    </v-container>
  </form>
</template>

<script>
import { required } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import SupportService from "@/services/work-organization/support-service";

export default {
  name: "SupportDayForm",
  mixins: [FormMixin({ service: SupportService })],
  validations: {
    item: {
      user: { required },
    },
  },
  data() {
    return {
      saveFunctionName: "update",
      successMessage: "Día de soporte guardado correctamente",
    };
  },
};
</script>
