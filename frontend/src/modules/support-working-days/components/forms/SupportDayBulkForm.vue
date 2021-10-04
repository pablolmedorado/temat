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
        <UserAutocomplete
          v-model.number="item.user"
          label="Usuario*"
          prepend-icon="mdi-account"
          show-random-btn
          :error-messages="buildValidationErrorMessages($v.items.$each.$iter[index].user)"
          @change="$v.items.$each.$iter[index].user.$touch()"
          @blur="$v.items.$each.$iter[index].user.$touch()"
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { minLength, required } from "vuelidate/lib/validators";

import BulkFormMixin from "@/mixins/bulk-form-mixin";

import SupportService from "@/modules/support-working-days/services/support-service";

export default {
  name: "SupportDayBulkForm",
  mixins: [BulkFormMixin({ service: SupportService })],
  validations: {
    items: {
      required,
      minLength: minLength(1),
      $each: {
        date: { required },
        user: { required },
      },
    },
  },
};
</script>
