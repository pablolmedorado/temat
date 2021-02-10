<template>
  <v-menu
    :disabled="!isTruncated"
    :close-on-content-click="false"
    :open-on-hover="true"
    :nudge-width="200"
    max-width="400px"
    offset-x
  >
    <template #activator="{ on, attrs }">
      <span :style="{ cursor }" v-bind="attrs" v-on="on">
        {{ text }}
      </span>
    </template>
    <v-card>
      <v-card-text class="text-pre-wrap">{{ value }}</v-card-text>
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
      default: "",
    },
    textLength: {
      type: Number,
      default: 30,
    },
  },
  computed: {
    isTruncated() {
      return this.value.length > this.textLength;
    },
    text() {
      return truncate(this.value, this.textLength);
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
