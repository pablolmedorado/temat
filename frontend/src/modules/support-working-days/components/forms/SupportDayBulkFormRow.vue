<template>
  <v-row>
    <v-col>
      <v-text-field
        :value="innerValue.date"
        label="Fecha*"
        prepend-icon="mdi-calendar"
        readonly
        :error-messages="getErrorMsgs(v$.innerValue.date)"
      />
    </v-col>
    <v-col>
      <UserAutocomplete
        v-model.number="innerValue.user"
        label="Usuario*"
        prepend-icon="mdi-account"
        show-random-btn
        :error-messages="getErrorMsgs(v$.innerValue.user)"
      />
    </v-col>
  </v-row>
</template>

<script>
import { required } from "@vuelidate/validators";

import useValidations from "@/composables/useValidations";
import useInnerValue from "@/composables/useInnerValue";

export default {
  name: "SupportDayBulkFormRow",
  props: {
    value: {
      type: Object,
      required: true,
    },
  },
  validations() {
    return {
      innerValue: {
        date: { required },
        user: { required },
      },
    };
  },
  setup(props) {
    const { v$, getErrorMsgs } = useValidations();
    const { innerValue } = useInnerValue(props);

    return {
      v$,
      getErrorMsgs,
      innerValue,
    };
  },
};
</script>
