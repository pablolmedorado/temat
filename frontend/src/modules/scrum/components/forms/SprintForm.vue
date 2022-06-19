<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.name"
          label="Nombre*"
          prepend-icon="mdi-format-title"
          counter="200"
          :error-messages="getErrorMsgs(v$.item.name)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6">
        <DatePickerInput
          v-model="item.start_date"
          label="Fecha de inicio*"
          prepend-icon="mdi-calendar-start"
          :error-messages="getErrorMsgs(v$.item.start_date)"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <DatePickerInput
          v-model="item.end_date"
          label="Fecha de fin*"
          prepend-icon="mdi-calendar-end"
          :error-messages="getErrorMsgs(v$.item.end_date)"
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
          :error-messages="getErrorMsgs(v$.item.accountable_user)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <TagAutocomplete v-model="item.tags" label="Tags" prepend-icon="mdi-label" multiple chips deletable-chips />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { watch } from "@vue/composition-api";
import { maxLength, required } from "@vuelidate/validators";
import { DateTime } from "luxon";

import SprintService from "@/modules/scrum/services/sprint-service";

import { useForm, formProps } from "@/composables/form";

export default {
  name: "SprintForm",
  props: formProps,
  validations() {
    return {
      item: {
        name: { required, maxLength: maxLength(200) },
        start_date: { required },
        end_date: {
          required,
          endDateBeforeStartDate: (value, siblings) => {
            const startDateAux = DateTime.fromISO(siblings.start_date);
            const endDateAux = DateTime.fromISO(value);
            return endDateAux.diff(startDateAux).milliseconds >= 0;
          },
        },
        accountable_user: { required },
      },
    };
  },
  setup() {
    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(SprintService, {
      successMessage: "Sprint guardado correctamente",
      customErrorMsgs: {
        endDateBeforeStartDate: "Fecha de fin anterior a la de inicio",
      },
    });

    // Watchers
    watch(
      () => item.value.start_date,
      (newDate, oldDate) => {
        if (oldDate && item.value.end_date) {
          const newDateAux = DateTime.fromISO(newDate);
          const oldDateAux = DateTime.fromISO(oldDate);
          const endDate = DateTime.fromISO(item.value.end_date);

          const previousDiff = endDate.diff(oldDateAux);
          const newEndDate = newDateAux.plus(previousDiff);
          item.value.end_date = newEndDate.toISODate();
        }
      }
    );

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
