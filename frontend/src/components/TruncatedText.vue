<template>
  <v-menu
    :disabled="!isTruncated"
    :close-on-content-click="false"
    :nudge-width="200"
    open-on-hover
    max-width="400px"
    offset-x
  >
    <template #activator="{ on, attrs }">
      <span :style="{ cursor }" v-bind="attrs" v-on="on">
        {{ truncatedText }}
      </span>
    </template>
    <v-card>
      <v-card-text class="text-pre-wrap">{{ text }}</v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { get } from "lodash";

import { truncate } from "@/filters";

export default {
  name: "TruncatedText",
  props: {
    value: {
      type: String,
      default: "",
    },
    textLength: {
      type: Number,
      default: 30,
    },
  },
  computed: {
    text() {
      return this.value || get(this.$slots, ["default", 0, "text"], "");
    },
    truncatedText() {
      return truncate(this.text, this.textLength);
    },
    isTruncated() {
      return this.text.length > this.textLength;
    },
    cursor() {
      return this.isTruncated ? "help" : "default";
    },
  },
};
</script>

<style scoped>
.text-pre-wrap {
  white-space: pre-wrap;
}
</style>
