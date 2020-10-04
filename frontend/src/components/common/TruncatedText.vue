<template>
  <v-menu
    :disabled="value.length <= textLength"
    :close-on-content-click="false"
    :open-on-hover="true"
    :nudge-width="200"
    max-width="400px"
    offset-x
  >
    <template #activator="{ on, attrs }">
      <span v-bind="attrs" v-on="on">{{ value | truncate(textLength) }}</span>
    </template>
    <v-card>
      <v-card-text>{{ value }}</v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { truncate } from "@/filters";

export default {
  name: "TruncatedText",
  filters: { truncate },
  props: {
    value: {
      type: String,
      default: ""
    },
    textLength: {
      type: Number,
      default: 30
    }
  }
};
</script>
