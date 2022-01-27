<template>
  <v-form v-if="item" ref="itemForm" :disabled="isTaskLoading('submit')">
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.label"
          label="Etiqueta"
          prepend-icon="mdi-tag"
          counter="100"
          :error-messages="buildValidationErrorMessages($v.item.label)"
          @input="$v.item.label.$touch()"
          @blur="$v.item.label.$touch()"
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
import { maxLength, required } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import GreenWorkingDayService from "@/modules/green-working-days/services/green-working-day-service";

export default {
  name: "GreenWorkingDayForm",
  mixins: [FormMixin({ service: GreenWorkingDayService })],
  validations: {
    item: {
      label: { required, maxLength: maxLength(100) },
    },
  },
  data() {
    return {
      saveFunctionName: "update",
      successMessage: "Jornada especial guardada correctamente",
    };
  },
};
</script>
