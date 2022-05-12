<template>
  <v-form ref="itemsForm" :disabled="isFormLoading">
    <SupportDayBulkFormRow v-for="index in items.length" :key="items[index - 1].date" v-model="items[index - 1]" />
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { minLength, required } from "@vuelidate/validators";

import SupportService from "@/modules/support-working-days/services/support-service";

import SupportDayBulkFormRow from "@/modules/support-working-days/components/forms/SupportDayBulkFormRow";

import { useBulkForm, bulkFormProps } from "@/composables/bulk-form";

export default {
  name: "SupportDayBulkForm",
  components: { SupportDayBulkFormRow },
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
    const { v$, getErrorMsgs, items, itemHaveChanged, submit, reset, isFormLoading } = useBulkForm(SupportService);

    return {
      // State
      items,
      // Computed
      v$,
      itemHaveChanged,
      isFormLoading,
      // Methods
      getErrorMsgs,
      submit,
      reset,
    };
  },
};
</script>
