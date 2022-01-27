<template>
  <v-form ref="itemsForm" :disabled="isTaskLoading('submit')">
    <v-row v-for="(item, index) in items" :key="item.date">
      <v-col>
        <v-text-field
          :value="item.date"
          label="Fecha*"
          prepend-icon="mdi-calendar"
          readonly
          :error-messages="buildValidationErrorMessages($v.items.$each.$iter[index].date)"
          @change="$v.items.$each.$iter[index].date.$touch()"
          @blur="$v.items.$each.$iter[index].date.$touch()"
        />
      </v-col>
      <v-col>
        <v-text-field
          v-model="item.label"
          label="Etiqueta"
          counter="100"
          prepend-icon="mdi-tag"
          :error-messages="buildValidationErrorMessages($v.items.$each.$iter[index].label)"
          @change="$v.items.$each.$iter[index].label.$touch()"
          @blur="$v.items.$each.$iter[index].label.$touch()"
        />
      </v-col>
      <v-col>
        <UserAutocomplete
          v-model="item.users"
          label="Usuarios"
          prepend-icon="mdi-account"
          multiple
          truncate-results
          show-random-btn
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { maxLength, minLength, required } from "vuelidate/lib/validators";

import BulkFormMixin from "@/mixins/bulk-form-mixin";

import GreenWorkingDayService from "@/modules/green-working-days/services/green-working-day-service";

export default {
  name: "GreenWorkingDayBulkForm",
  mixins: [BulkFormMixin({ service: GreenWorkingDayService })],
  validations: {
    items: {
      required,
      minLength: minLength(1),
      $each: {
        date: { required },
        label: { required, maxLength: maxLength(100) },
      },
    },
  },
};
</script>
