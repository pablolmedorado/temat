<template>
  <form v-if="item" ref="itemForm">
    <v-container>
      <v-row>
        <v-col>
          <v-text-field
            v-model="item.name"
            label="Nombre*"
            prepend-icon="mdi-format-title"
            counter="200"
            :error-messages="buildValidationErrorMessages($v.item.name)"
            @input="$v.item.name.$touch()"
            @blur="$v.item.name.$touch()"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6">
          <DatePickerInput
            v-model="item.start_date"
            label="Fecha de inicio*"
            prepend-icon="mdi-calendar-start"
            :error-messages="buildValidationErrorMessages($v.item.start_date)"
            @input="$v.item.start_date.$touch()"
            @blur="$v.item.start_date.$touch()"
          />
        </v-col>
        <v-col cols="12" sm="6">
          <DatePickerInput
            v-model="item.end_date"
            label="Fecha de fin*"
            prepend-icon="mdi-calendar-end"
            :error-messages="buildValidationErrorMessages($v.item.end_date)"
            @input="$v.item.end_date.$touch()"
            @blur="$v.item.end_date.$touch()"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <UserAutocomplete
            v-model.number="item.accountable_user"
            label="Usuario responsable*"
            prepend-icon="mdi-account-tie"
            show-random-btn
            :error-messages="buildValidationErrorMessages($v.item.accountable_user)"
            @change="$v.item.accountable_user.$touch()"
            @blur="$v.item.accountable_user.$touch()"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <TagAutocomplete v-model="item.tags" label="Tags" prepend-icon="mdi-label" multiple chips deletable-chips />
        </v-col>
      </v-row>
      <small>* indica campo obligatorio</small>
    </v-container>
  </form>
</template>

<script>
import { mapState } from "vuex";
import { DateTime } from "luxon";
import { maxLength, required } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import SprintService from "@/services/scrum/sprint-service";

export default {
  name: "SprintForm",
  mixins: [FormMixin({ service: SprintService })],
  validations: {
    item: {
      name: { required, maxLength: maxLength(200) },
      start_date: { required },
      end_date: {
        required,
        endDateBeforeStartDate: (value, vm) => {
          const startDateAux = DateTime.fromISO(vm.start_date);
          const endDateAux = DateTime.fromISO(vm.end_date);
          return endDateAux.diff(startDateAux).milliseconds >= 0;
        },
      },
      accountable_user: { required },
    },
  },
  data() {
    return {
      validationErrorMessages: {
        endDateBeforeStartDate: "Fecha de fin anterior a la de inicio",
      },
      successMessage: "Sprint guardado correctamente",
    };
  },
  computed: {
    ...mapState(["locale"]),
  },
  watch: {
    "item.start_date": {
      handler(newDate, oldDate) {
        if (oldDate && this.item.end_date) {
          const newDateAux = DateTime.fromISO(newDate);
          const oldDateAux = DateTime.fromISO(oldDate);
          const endDate = DateTime.fromISO(this.item.end_date);

          const previousDiff = endDate.diff(oldDateAux);
          const newEndDate = newDateAux.plus(previousDiff);
          this.item.end_date = newEndDate.toISODate();
        }
      },
    },
  },
};
</script>
