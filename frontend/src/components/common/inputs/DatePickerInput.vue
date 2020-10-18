<template>
  <v-menu
    v-model="showDatepicker"
    :close-on-content-click="false"
    :nudge-right="40"
    transition="scale-transition"
    offset-y
    min-width="290px"
  >
    <template #activator="{ on, attrs }">
      <v-text-field
        :value="value | date"
        :label="label"
        :prepend-icon="prependIcon"
        :append-icon="appendIcon"
        :rules="rules"
        :error-messages="errorMessages"
        :clearable="clearable && !readonly"
        readonly
        v-bind="attrs"
        @blur="$emit('blur', $event)"
        @click:append="$emit('click:append', $event)"
        @click:clear="$emit('input', null)"
        v-on="on"
      ></v-text-field>
    </template>
    <v-date-picker
      :value="value"
      :readonly="readonly"
      :min="min"
      :max="max"
      :locale="locale"
      :locale-first-day-of-year="4"
      first-day-of-week="1"
      color="primary"
      show-week
      no-title
      @input="showDatepicker = false"
      @change="$emit('input', $event)"
    />
  </v-menu>
</template>

<script>
import { mapState } from "vuex";

import { isoDateToLocaleString } from "@/utils/dates";

export default {
  name: "DatePickerInput",
  filters: {
    date: isoDateToLocaleString,
  },
  inheritAttrs: false,
  props: {
    value: {
      type: String,
      default: null,
    },
    label: {
      type: String,
      default: "",
    },
    prependIcon: {
      type: String,
      default: undefined,
    },
    appendIcon: {
      type: String,
      default: undefined,
    },
    min: {
      type: String,
      default: undefined,
    },
    max: {
      type: String,
      default: undefined,
    },
    rules: {
      type: Array,
      default: () => [],
    },
    errorMessages: {
      type: Array,
      default: () => [],
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showDatepicker: false,
    };
  },
  computed: {
    ...mapState(["locale"]),
  },
};
</script>
