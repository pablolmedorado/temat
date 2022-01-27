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
import { mapState } from "pinia";

import FilterMixin from "@/mixins/filter-mixin";

import { useMainStore } from "@/stores/main";

export default {
  name: "HolidayFilters",
  mixins: [FilterMixin],
  data() {
    return {
      approvedOptions: [
        { label: "Sí", value: true },
        { label: "No", value: false },
      ],
    };
  },
  computed: {
    ...mapState(useMainStore, ["yearOptions"]),
    userFilter() {
      return this.splitFilterValue("user_id__in", true);
    },
  },
  methods: {
    reset() {
      this.filters.user_id__in = "";
    },
  },
};
</script>
