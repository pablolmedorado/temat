<template>
  <v-row>
    <v-col cols="6" md="3">
      <v-combobox
        :value="filters.planned_date__year"
        :items="yearOptions"
        label="Año"
        prepend-icon="mdi-calendar-range"
        clearable
        @change="updateFilters({ planned_date__year: $event })"
      />
    </v-col>
    <v-col cols="6" md="4">
      <UserAutocomplete
        :value="userFilter"
        label="Usuarios"
        prepend-icon="mdi-account"
        multiple
        truncate-results
        clearable
        @input="updateFilters({ user_id__in: $event.join(',') })"
      />
    </v-col>
    <v-col cols="6" md="3">
      <v-select
        :value="filters.approved__isnull"
        :items="approvedOptions"
        item-text="label"
        item-value="value"
        label="Pendientes"
        prepend-icon="mdi-timer-sand"
        clearable
        @change="updateFilters({ approved__isnull: $event })"
      />
    </v-col>
    <v-col cols="6" md="2">
      <v-btn class="my-2" color="primary" :disabled="disabled" @click="$emit('apply:filters')"> Filtrar </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import { computed, toRefs } from "@vue/composition-api";

import { useMainStore } from "@/stores/main";

import { useFilters, filterProps } from "@/composables/filters";

export default {
  name: "HolidayFilters",
  props: filterProps,
  setup() {
    // Store
    const store = useMainStore();

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
    const approvedOptions = [
      { label: "Sí", value: true },
      { label: "No", value: false },
    ];

    // Computed
    const { yearOptions } = toRefs(store);
    const userFilter = computed(() => splitFilterValue("user_id__in", true));

    // Methods
    function reset() {
      updateFilters({ user_id__in: "" });
    }

    return {
      // State
      showFiltersDialog,
      hasAdvancedFilters,
      approvedOptions,
      // Computed
      yearOptions,
      userFilter,
      // Methods
      updateFilters,
      clearFilters,
      openFiltersDialog,
      closeFiltersDialog,
      applyFiltersFromDialog,
      reset,
    };
  },
};
</script>
