<template>
  <span>
    <v-chip
      v-for="tag in tags"
      :key="camelCase(tag.name)"
      class="mr-1 my-1"
      v-bind="$attrs"
      :color="tag.colour"
      :dark="applyDarkVariant(tag.colour)"
      :small="small"
      label
      @click="$emit('click:tag', tag.name)"
    >
      <v-icon :small="small" left>{{ tag.icon }}</v-icon>
      {{ tag.name | truncate(20) }}
    </v-chip>
  </span>
</template>

<script>
import { camelCase } from "lodash";

import { truncate } from "@/filters";
import { applyDarkVariant } from "@/utils/colours";

export default {
  name: "TagLabels",
  filters: {
    truncate,
  },
  inheritAttrs: false,
  props: {
    tags: {
      type: Array,
      required: true,
    },
    small: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    camelCase,
    applyDarkVariant,
  },
};
</script>
