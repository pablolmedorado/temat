<template>
  <v-form ref="itemsForm" :disabled="isFormLoading">
    <GreenWorkingDayBulkFormRow v-for="index in items.length" :key="items[index - 1].date" v-model="items[index - 1]" />
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { minLength, required } from "@vuelidate/validators";

import GreenWorkingDayService from "@/modules/green-working-days/services/green-working-day-service";

import GreenWorkingDayBulkFormRow from "@/modules/green-working-days/components/forms/GreenWorkingDayBulkFormRow";

import { useBulkForm, bulkFormProps } from "@/composables/bulk-form";

export default {
  name: "GreenWorkingDayBulkForm",
  components: { GreenWorkingDayBulkFormRow },
  props: bulkFormProps,
  validations() {
    return {
      items: {
        required,
        minLength: minLength(1),
      },
    };
  },
  setup() {
    const { v$, getErrorMsgs, items, itemHaveChanged, submit, reset, isFormLoading } =
      useBulkForm(GreenWorkingDayService);

    return {
      v$,
      getErrorMsgs,
      items,
      itemHaveChanged,
      submit,
      reset,
      isFormLoading,
    };
  },
};
</script>
