<template>
  <div>
    <v-breadcrumbs v-if="items.length" :items="items">
      <template #item="{ item }">
        <v-breadcrumbs-item v-bind="item">
          {{ item.text | truncate(50) }}
        </v-breadcrumbs-item>
      </template>
    </v-breadcrumbs>
    <v-skeleton-loader v-else type="heading" class="pl-6 pr-4 py-4" />
  </div>
</template>

<script>
import { truncate } from "@/utils/text";

export default {
  name: "ContextBreadcrumbs",
  filters: { truncate },
  props: {
    items: {
      type: Array,
      default: () => [],
    },
  },
};
</script>
