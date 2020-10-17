<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <DatePickerInput
          v-model="filters.date__gte"
          label="Fecha inicio"
          prepend-icon="mdi-calendar-arrow-right"
          clearable
        />
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <DatePickerInput
          v-model="filters.date__lte"
          label="Fecha fin"
          prepend-icon="mdi-calendar-arrow-left"
          clearable
        />
      </v-col>
      <v-col v-if="loggedUser.is_staff" cols="12" sm="6" md="3">
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
        <v-btn class="my-2" color="primary" :loading="loading" :disabled="loading" @click="$emit('apply:filters')">
          Filtrar
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";

import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "EffortFilters",
  mixins: [FilterMixin],
  computed: {
    ...mapState(["loggedUser"]),
    userFilter() {
      return this.splitFilterValue("user_id__in", true);
    },
  },
};
</script>
