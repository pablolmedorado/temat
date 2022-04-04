<template>
  <v-menu
    v-model="showDatePicker"
    :disabled="readonly"
    :close-on-content-click="false"
    :nudge-right="40"
    transition="scale-transition"
    offset-y
    min-width="290px"
  >
    <template #activator="{ on, attrs }">
      <v-text-field
        v-bind="{ ...attrs, ...$attrs }"
        :value="value | date"
        :clearable="clearable && !readonly"
        readonly
        @click:clear="$emit('input', null)"
        v-on="{ ...on, ...$listeners }"
      >
        <template #append>
          <slot name="append"></slot>
        </template>
        <template #append-outer>
          <slot name="append-outer"></slot>
        </template>
      </v-text-field>
    </template>
    <v-date-picker
      :value="value"
      :min="min"
      :max="max"
      :locale="locale"
      :locale-first-day-of-year="4"
      first-day-of-week="1"
      color="primary"
      show-week
      no-title
      scrollable
      @input="showDatePicker = false"
      @change="$emit('input', $event)"
    />
  </v-menu>
</template>

<script>
import { ref, toRefs } from "@vue/composition-api";

import { useMainStore } from "@/stores/main";

import { isoDateToLocaleString } from "@/utils/dates";

export default {
  name: "DatePickerInput",
  filters: {
    date: isoDateToLocaleString,
  },
  inheritAttrs: false,
  props: {
    value: {
      type: [Array, String],
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
    readonly: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    // Store
    const store = useMainStore();

    // State
    const showDatePicker = ref(false);

    // Computed
    const { locale } = toRefs(store);

    return {
      showDatePicker,
      locale,
    };
  },
};
</script>
