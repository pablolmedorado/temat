<template>
  <div>
    <v-row>
      <v-col cols="12" sm="5" lg="4">
        <v-text-field
          :value="filters.search"
          label="Buscar"
          placeholder="Nombre"
          prepend-icon="mdi-magnify"
          clearable
          @input="updateFilters({ search: $event })"
          @keyup.enter="$emit('apply:filters')"
        />
      </v-col>
      <v-col cols="12" sm="4" lg="3">
        <v-select
          :value="filters.ongoing"
          :items="ongoingOptions"
          item-text="label"
          item-value="value"
          label="En curso"
          prepend-icon="mdi-calendar-arrow-right"
          clearable
          @change="updateFilters({ ongoing: $event })"
        />
      </v-col>
      <v-col cols="12" sm="3" lg="2">
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
        <v-toolbar flat>
          <v-toolbar-title class="text-h6"> Filtros avanzados </v-toolbar-title>
        </v-toolbar>
        <v-card-text>
          <v-row>
            <v-col>
              <v-text-field
                :value="filters.search"
                label="Buscar"
                placeholder="Nombre"
                prepend-icon="mdi-magnify"
                clearable
                @input="updateFilters({ search: $event })"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-select
                :value="filters.ongoing"
                :items="ongoingOptions"
                item-text="label"
                item-value="value"
                label="En curso"
                prepend-icon="mdi-calendar-arrow-right"
                clearable
                @change="updateFilters({ ongoing: $event })"
              />
            </v-col>
            <v-col>
              <UserAutocomplete
                :value="filters.accountable_user_id"
                label="Usuario responsable"
                prepend-icon="mdi-account-tie"
                clearable
                @input="updateFilters({ accountable_user_id: $event })"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <DatePickerInput
                :value="filters.start_date__gte"
                label="Fecha desde"
                prepend-icon="mdi-calendar-start"
                clearable
                @input="updateFilters({ start_date__gte: $event })"
              />
            </v-col>
            <v-col>
              <DatePickerInput
                :value="filters.end_date__lte"
                label="Fecha hasta"
                prepend-icon="mdi-calendar-end"
                clearable
                @input="updateFilters({ end_date__lte: $event })"
              />
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
        <v-divider />
        <v-card-actions>
          <v-btn color="warning" text @click="clearFilters">Limpiar</v-btn>
          <v-spacer />
          <v-btn text @click="closeFiltersDialog"> Volver </v-btn>
          <v-btn text :loading="loading" :disabled="loading" @click="applyFiltersFromDialog"> Filtrar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "SprintFilters",
  mixins: [FilterMixin],
  data() {
    return {
      basicFilters: ["ongoing", "accountable_user_id"],
      ongoingOptions: [
        { label: "Sí", value: true },
        { label: "No", value: false },
      ],
    };
  },
  computed: {
    tagFilter() {
      return this.splitFilterValue("tags__name__in");
    },
  },
};
</script>
