<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field
          :value="filters.search"
          label="Buscar"
          placeholder="Nombre"
          prepend-icon="mdi-magnify"
          clearable
          @input="updateFilters({ search: $event })"
          @keyup.enter="$emit('apply:filters')"
        ></v-text-field>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <UserAutocomplete
          :value="filters.accountable_user_id"
          label="Usuario responsable"
          prepend-icon="mdi-account-tie"
          clearable
          @click:clear="updateFilters({ accountable_user_id: null })"
          @input="updateFilters({ accountable_user_id: $event })"
        />
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-btn class="my-2" color="primary" :loading="loading" :disabled="loading" @click="$emit('apply:filters')">
          Filtrar
        </v-btn>
      </v-col>
    </v-row>

    <v-dialog
      v-model="showFiltersDialog"
      max-width="700"
      scrollable
      @click:outside="closeFiltersDialog"
      @keydown.esc="closeFiltersDialog"
    >
      <v-card>
        <v-card-title class="text-h6">Filtros avanzados</v-card-title>
        <v-card-text>
          <v-row>
            <v-col>
              <DatePickerInput
                :value="filters.start_date__gte"
                label="Fecha desde"
                prepend-icon="mdi-calendar-arrow-right"
                clearable
                @input="updateFilters({ start_date__gte: $event })"
              ></DatePickerInput>
            </v-col>
            <v-col>
              <DatePickerInput
                :value="filters.end_date__lte"
                label="Fecha hasta"
                prepend-icon="mdi-calendar-arrow-left"
                clearable
                @input="updateFilters({ end_date__lte: $event })"
              ></DatePickerInput>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <TagAutocomplete
                :value="tagFilter"
                label="Tags"
                prepend-icon="mdi-label"
                multiple
                chips
                deletable-chips
                clearable
                @input="updateFilters({ tags__name__in: $event.join(',') })"
              />
            </v-col>
          </v-row>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn color="warning" text @click="$emit('reset:filters')">Restablecer</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="closeFiltersDialog">
            Volver
          </v-btn>
          <v-btn color="primary" text :loading="loading" :disabled="loading" @click="applyFiltersFromDialog">
            Filtrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "SprintFilters",
  mixins: [FilterMixin],
  data() {
    return {
      basicFilters: ["search", "accountable_user_id"]
    };
  },
  computed: {
    tagFilter() {
      return this.splitFilterValue("tags__name__in");
    }
  }
};
</script>
