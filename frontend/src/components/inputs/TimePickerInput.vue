<template>
  <v-menu
    ref="timePicker"
    v-model="showTimePicker"
    :disabled="readonly"
    :close-on-content-click="false"
    :nudge-right="40"
    :return-value.sync="innerValue"
    transition="scale-transition"
    offset-y
    width="290px"
  >
    <template #activator="{ on, attrs }">
      <v-text-field
        v-bind="{ ...attrs, ...$attrs }"
        :value="innerValue"
        :clearable="clearable && !readonly"
        readonly
        @click:clear="innerValue = null"
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
    <v-time-picker
      v-if="showTimePicker"
      v-model="innerValue"
      format="24hr"
      color="primary"
      scrollable
      @click:minute="$refs.timePicker.save(innerValue)"
    />
  </v-menu>
</template>

<script>
import { ref } from "@vue/composition-api";
import { useVModel } from "@vueuse/core";

export default {
  name: "TimePickerInput",
  inheritAttrs: false,
  props: {
    value: {
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
  setup(props) {
    // Composables
    const innerValue = useVModel(props);

    // State
    const showTimePicker = ref(false);

    return {
      showTimePicker,
      innerValue,
    };
  },
};
</script>
