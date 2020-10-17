<template>
  <span>
    <v-chip v-for="tag in tags" :key="tag" class="mr-1 my-1" color="info" label small @click="$emit('click:tag', tag)">
      <v-icon small left>mdi-label</v-icon>
      {{ tag | truncate(20) }}
    </v-chip>
  </span>
</template>

<script>
import { truncate } from "@/filters";

export default {
  name: "TagLabels",
  filters: {
    truncate,
  },
  props: {
    tags: {
      type: Array,
      required: true,
    },
  },
};
</script>
