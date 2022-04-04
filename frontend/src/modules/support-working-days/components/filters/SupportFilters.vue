<template>
  <v-row>
    <v-col cols="12" sm="6" md="3">
      <DatePickerInput
        :value="filters.date__gte"
        label="Fecha inicio"
        prepend-icon="mdi-calendar-start"
        clearable
        @input="updateFilters({ date__gte: $event })"
      />
    </v-col>
    <v-col cols="12" sm="6" md="3">
      <DatePickerInput
        :value="filters.date__lte"
        label="Fecha fin"
        prepend-icon="mdi-calendar-end"
        clearable
        @input="updateFilters({ date__lte: $event })"
      />
    </v-col>
    <v-col cols="12" sm="6" md="3">
      <UserAutocomplete
        :value="filters.user_id"
        label="Usuario"
        prepend-icon="mdi-account"
        clearable
        @input="updateFilters({ user_id: $event })"
      />
    </v-col>
    <v-col cols="12" sm="6" md="3">
      <v-btn class="my-2" color="primary" :disabled="disabled" @click="$emit('apply:filters')"> Filtrar </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import useFilters, { filterProps } from "@/composables/useFilters";

export default {
  name: "SupportFilters",
  props: filterProps,
  setup(props) {
    // Composables
    const {
      showFiltersDialog,
      hasAdvancedFilters,
      updateFilters,
      clearFilters,
      openFiltersDialog,
      closeFiltersDialog,
      applyFiltersFromDialog,
    } = useFilters(props);

    return {
      // State
      showFiltersDialog,
      hasAdvancedFilters,
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
