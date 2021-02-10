<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col cols="12" md="4" lg="5">
        <v-text-field
          :value="filters.search"
          label="Buscar"
          placeholder="Título, detalles"
          prepend-icon="mdi-magnify"
          clearable
          @input="updateFilters({ search: $event })"
          @keyup.enter="$emit('apply:filters')"
        />
      </v-col>
      <v-col cols="6" md="4" lg="3">
        <v-select
          :value="typeFilter"
          :items="eventTypesOptions.filter((type) => !type.system)"
          :loading="!eventTypesOptions.length"
          item-text="name"
          item-value="id"
          label="Tipo"
          prepend-icon="mdi-shape"
          multiple
          clearable
          @input="updateFilters({ type_id__in: $event.join(',') })"
        />
      </v-col>
      <v-col cols="6" md="4">
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
                placeholder="Título, detalles"
                prepend-icon="mdi-magnify"
                clearable
                @input="updateFilters({ search: $event })"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <DatePickerInput
                :value="filters.start_datetime__date__gte"
                label="Fecha (desde)"
                prepend-icon="mdi-calendar-start"
                clearable
                @input="updateFilters({ start_datetime__date__gte: $event })"
              />
            </v-col>
            <v-col>
              <DatePickerInput
                :value="filters.end_datetime__date__lte"
                label="Fecha (hasta)"
                prepend-icon="mdi-calendar-end"
                clearable
                @input="updateFilters({ end_datetime__date__lte: $event })"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-select
                :value="typeFilter"
                :items="eventTypesOptions.filter((type) => !type.system)"
                :loading="!eventTypesOptions.length"
                item-text="name"
                item-value="id"
                label="Tipo"
                prepend-icon="mdi-shape"
                multiple
                clearable
                @input="updateFilters({ type_id__in: $event.join(',') })"
              />
            </v-col>
            <v-col>
              <v-select
                :value="filters.visibility"
                :items="visibilityOptions"
                item-text="label"
                item-value="value"
                label="Visibilidad"
                prepend-icon="mdi-eye"
                clearable
                @input="updateFilters({ visibility: $event })"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <UserAutocomplete
                :value="attendeeFilter"
                label="Usuarios asistentes"
                prepend-icon="mdi-account"
                multiple
                chips
                deletable-chips
                clearable
                @input="updateFilters({ attendees__id__in: $event.join(',') })"
              />
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <GroupAutocomplete
                :value="groupFilter"
                label="Grupos asistentes"
                prepend-icon="mdi-account-group"
                multiple
                chips
                deletable-chips
                clearable
                @input="updateFilters({ groups__id__in: $event.join(',') })"
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
          <v-btn color="warning" text @click="$emit('clear:filters')">Limpiar</v-btn>
          <v-spacer />
          <v-btn color="primary" text @click="closeFiltersDialog"> Volver </v-btn>
          <v-btn color="primary" text :loading="loading" :disabled="loading" @click="applyFiltersFromDialog">
            Filtrar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import { mapState } from "vuex";

import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "EventFilters",
  mixins: [FilterMixin],
  data() {
    return {
      basicFilters: ["search", "type_id__in"],
    };
  },
  computed: {
    ...mapState("calendar", {
      eventTypesOptions: "eventTypes",
      visibilityOptions: "eventVisibilityTypes",
    }),
    typeFilter() {
      return this.splitFilterValue("type_id__in", true);
    },
    attendeeFilter() {
      return this.splitFilterValue("attendees__id__in", true);
    },
    groupFilter() {
      return this.splitFilterValue("groups__id__in", true);
    },
    tagFilter() {
      return this.splitFilterValue("tags__name__in");
    },
  },
};
</script>
