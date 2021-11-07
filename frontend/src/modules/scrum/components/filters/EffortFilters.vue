<template>
  <v-row>
    <v-col cols="12" sm="6" md="3">
      <DatePickerInput v-model="filters.date__gte" label="Fecha inicio" prepend-icon="mdi-calendar-start" clearable />
    </v-col>
    <v-col cols="12" sm="6" md="3">
      <DatePickerInput v-model="filters.date__lte" label="Fecha fin" prepend-icon="mdi-calendar-end" clearable />
    </v-col>
    <v-col v-if="showUserFilter" cols="12" sm="6" md="3">
      <UserAutocomplete
        :value="userFilter"
        label="Usuario"
        prepend-icon="mdi-account"
        multiple
        truncate-results
        clearable
        @input="updateFilters({ user_id__in: $event.join(',') })"
      />
    </v-col>
    <v-col cols="12" sm="6" md="3">
      <v-btn class="my-2" color="primary" :disabled="disabled" @click="$emit('apply:filters')"> Filtrar </v-btn>
    </v-col>
  </v-row>
</template>

<script>
import FilterMixin from "@/mixins/filter-mixin";

import { userHasPermission } from "@/utils/permissions";

export default {
  name: "EffortFilters",
  mixins: [FilterMixin],
  computed: {
    showUserFilter() {
      return userHasPermission("scrum.view_effort");
    },
    userFilter() {
      return this.splitFilterValue("user_id__in", true);
    },
  },
};
</script>
