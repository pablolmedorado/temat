<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <DatePickerInput
          :value="filters.date__gte"
          label="Fecha inicio"
          prepend-icon="mdi-calendar-arrow-right"
          clearable
          @input="updateFilters({ date__gte: $event })"
        ></DatePickerInput>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <DatePickerInput
          :value="filters.date__lte"
          label="Fecha fin"
          prepend-icon="mdi-calendar-arrow-left"
          clearable
          @input="updateFilters({ date__lte: $event })"
        ></DatePickerInput>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <UserAutocomplete
          :value="filters.user_id"
          label="Usuario"
          prepend-icon="mdi-account"
          clearable
          @click:clear="updateFilters({ user_id: null })"
          @input="updateFilters({ user_id: $event })"
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
import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "SupportFilters",
  mixins: [FilterMixin],
};
</script>
