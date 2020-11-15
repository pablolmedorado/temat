<template>
  <form ref="itemsForm">
    <v-container>
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
            v-model.number="item.main_user"
            label="Usuario principal"
            prepend-icon="mdi-account"
            show-random-btn
          />
        </v-col>
        <v-col>
          <UserAutocomplete
            v-model.number="item.support_user"
            label="Usuario de apoyo"
            prepend-icon="mdi-account-outline"
            show-random-btn
            :error-messages="buildValidationErrorMessages($v.items.$each.$iter[index].support_user)"
            @change="$v.items.$each.$iter[index].support_user.$touch()"
            @blur="$v.items.$each.$iter[index].support_user.$touch()"
          />
        </v-col>
      </v-row>
      <small>* indica campo obligatorio</small>
    </v-container>
  </form>
</template>

<script>
import { maxLength, minLength, not, required, sameAs } from "vuelidate/lib/validators";

import BulkFormMixin from "@/mixins/bulk-form-mixin";

import GreenService from "@/services/work-organization/green-service";

export default {
  name: "GreenWorkingDayBulkForm",
  mixins: [BulkFormMixin({ service: GreenService })],
  validations: {
    items: {
      required,
      minLength: minLength(1),
      $each: {
        date: { required },
        label: { maxLength: maxLength(100) },
        support_user: { notSameAsMainUser: not(sameAs("main_user")) },
      },
    },
  },
};
</script>
