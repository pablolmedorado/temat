<template>
  <v-autocomplete v-bind="{ ...$props, ...$attrs }" :items="tagOptions" :loading="!tagOptions.length" v-on="$listeners">
    <template v-if="truncateResults" #selection="{ item, index }">
      <v-chip v-if="index === 0" small>
        <span>{{ item }}</span>
      </v-chip>
      <span v-if="index === 1" class="grey--text text-caption">(+{{ value.length - 1 }} más)</span>
    </template>
  </v-autocomplete>
</template>

<script>
import { toRefs } from "@vue/composition-api";

import { useTagStore } from "@/stores/tags";

export default {
  name: "TagAutocomplete",
  inheritAttrs: false,
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    truncateResults: {
      type: Boolean,
      default: false,
    },
  },
  setup() {
    // Store
    const tagStore = useTagStore();

    // Computed
    const { tagFlatList: tagOptions } = toRefs(tagStore);

    return {
      tagOptions,
    };
  },
};
</script>
