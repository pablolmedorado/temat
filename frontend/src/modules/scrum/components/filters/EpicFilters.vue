<template>
  <v-row>
    <v-col cols="6" md="3">
      <v-text-field
        :value="filters.search"
        label="Buscar"
        prepend-icon="mdi-magnify"
        clearable
        @input="updateFilters({ search: $event })"
        @keyup.enter="$emit('apply:filters')"
      />
    </v-col>
    <v-col cols="6" md="3">
      <TagAutocomplete
        :value="tagFilter"
        label="Tags"
        prepend-icon="mdi-label"
        multiple
        truncate-results
        clearable
        @input="updateFilters({ tags__name__in: $event.join(',') })"
      />
    </v-col>
    <v-col cols="6" md="3">
      <v-select
        :value="filters.finished"
        :items="finishedOptions"
        item-text="label"
        item-value="value"
        label="Finalizada"
        prepend-icon="mdi-check-bold"
        clearable
        @change="updateFilters({ finished: $event })"
      />
    </v-col>
    <v-col cols="6" md="3">
      <v-btn class="my-2" color="primary" :disabled="disabled" @click="$emit('apply:filters')"> Filtrar </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import { computed } from "@vue/composition-api";

import { useFilters, filterProps } from "@/composables/filters";

export default {
  name: "EpicFilters",
  props: filterProps,
  setup() {
    // Composables
    const {
      showFiltersDialog,
      hasAdvancedFilters,
      updateFilters,
      clearFilters,
      openFiltersDialog,
      closeFiltersDialog,
      applyFiltersFromDialog,
      splitFilterValue,
    } = useFilters();

    // State
    const finishedOptions = [
      { label: "Sí", value: true },
      { label: "No", value: false },
    ];

    // Computed
    const tagFilter = computed(() => splitFilterValue("tags__name__in"));

    return {
      // State
      showFiltersDialog,
      hasAdvancedFilters,
      finishedOptions,
      // Computed
      tagFilter,
      // Methods
      updateFilters,
      clearFilters,
      openFiltersDialog,
      closeFiltersDialog,
      applyFiltersFromDialog,
    };
  },
};
</script>
