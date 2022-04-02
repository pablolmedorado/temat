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
      <v-text-field
        v-model="innerValue.label"
        label="Etiqueta"
        counter="100"
        prepend-icon="mdi-tag"
        :error-messages="getErrorMsgs(v$.innerValue.label)"
      />
    </v-col>
    <v-col>
      <UserAutocomplete
        v-model="innerValue.users"
        label="Usuarios"
        prepend-icon="mdi-account"
        multiple
        truncate-results
        show-random-btn
      />
    </v-col>
  </v-row>
</template>

<script>
import { maxLength, required } from "@vuelidate/validators";

import useValidations from "@/composables/useValidations";
import useInnerValue from "@/composables/useInnerValue";

export default {
  name: "GreenWorkingDayBulkFormRow",
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
        label: { required, maxLength: maxLength(100) },
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
