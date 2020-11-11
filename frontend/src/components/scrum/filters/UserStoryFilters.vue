<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col lg="3" sm="6" cols="12">
        <v-text-field
          :value="filters.search"
          label="Buscar"
          placeholder="Id, nombre, descripciones, comentarios, scv..."
          prepend-icon="mdi-magnify"
          clearable
          @input="updateFilters({ search: $event })"
          @keyup.enter="$emit('apply:filters')"
        ></v-text-field>
      </v-col>
      <v-col lg="4" sm="6" cols="12">
        <v-select
          :value="statusFilter"
          :items="userStoryStatusOptions"
          :loading="!userStoryStatusOptions.length"
          item-text="label"
          item-value="value"
          label="Estado"
          prepend-icon="mdi-state-machine"
          multiple
          clearable
          @input="updateFilters({ status__in: $event.join(',') })"
        >
          <template #selection="{ item, index }">
            <v-chip v-if="index === 0" small>
              <span>{{ item.label }}</span>
            </v-chip>
            <span v-if="index === 1" class="grey--text text-caption">(+{{ statusFilter.length - 1 }} más)</span>
          </template>
        </v-select>
      </v-col>
      <v-col lg="3" sm="6" cols="12">
        <UserAutocomplete
          :value="anyRoleUserFilter"
          label="Usuario (cualquier rol)"
          prepend-icon="mdi-account-multiple"
          multiple
          truncate-results
          clearable
          @input="updateFilters({ any_role_user__in: $event.join(',') })"
        />
      </v-col>
      <v-col lg="2" sm="6" cols="12">
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
          <v-tabs v-model="tab">
            <v-tab href="#general">General</v-tab>
            <v-tab href="#status">Estado</v-tab>
            <v-tab href="#dates">Fechas</v-tab>
            <v-tab href="#people">Personas</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item value="general">
              <v-row>
                <v-col>
                  <v-select
                    :value="filters.type_id"
                    :items="userStoryTypesOptions"
                    item-text="name"
                    item-value="id"
                    label="Tipo"
                    prepend-icon="mdi-shape"
                    :loading="!userStoryTypesOptions.length"
                    @input="updateFilters({ type_id: $event })"
                  ></v-select>
                </v-col>
                <v-col>
                  <v-select
                    :value="priorityFilter"
                    :items="priorityOptions"
                    label="Prioridad"
                    prepend-icon="mdi-priority-high"
                    multiple
                    clearable
                    @input="updateFilters({ priority__in: $event.join(',') })"
                  ></v-select>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <AsyncAutocomplete
                    :value="filters.sprint_id"
                    :service="sprintService"
                    search-field="name"
                    search-lookup="icontains"
                    :disabled="disableSprintFilter"
                    label="Sprint"
                    prepend-icon="mdi-run-fast"
                    @input="updateFilters({ sprint_id: $event })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <AsyncAutocomplete
                    :value="filters.epic_id"
                    :service="epicService"
                    search-field="name"
                    search-lookup="icontains"
                    :disabled="disableEpicFilter"
                    label="Épica"
                    prepend-icon="mdi-sword-cross"
                    @input="updateFilters({ epic_id: $event })"
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
              <v-row>
                <v-col>
                  <v-text-field
                    :value="filters.planned_effort__gte"
                    label="Esfuerzo (desde)"
                    type="number"
                    min="0"
                    prepend-icon="mdi-dumbbell"
                    clearable
                    @input="updateFilters({ planned_effort__gte: $event })"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    :value="filters.planned_effort__lte"
                    label="Esfuerzo (hasta)"
                    type="number"
                    min="0"
                    prepend-icon="mdi-dumbbell"
                    clearable
                    @input="updateFilters({ planned_effort__lte: $event })"
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-tab-item>
            <v-tab-item value="status">
              <v-row>
                <v-col>
                  <v-text-field
                    :value="filters.current_progress__gte"
                    label="Avance (desde)"
                    type="number"
                    min="0"
                    max="100"
                    prepend-icon="mdi-percent"
                    clearable
                    @input="updateFilters({ current_progress__gte: $event })"
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    :value="filters.current_progress__lte"
                    label="Avance (hasta)"
                    type="number"
                    min="0"
                    max="100"
                    prepend-icon="mdi-percent"
                    clearable
                    @input="updateFilters({ current_progress__lte: $event })"
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-select
                    :value="filters.risk_level"
                    :items="riskLevelOptions"
                    item-text="label"
                    item-value="value"
                    label="Nivel de riesgo"
                    prepend-icon="mdi-alert-decagram"
                    clearable
                    @input="updateFilters({ risk_level: $event })"
                  ></v-select>
                </v-col>
                <v-col>
                  <v-switch
                    :value="filters.validated"
                    true-value="false"
                    false-value=""
                    label="Validación rechazada"
                    inset
                    @change="updateFilters({ validated: $event })"
                  ></v-switch>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-switch
                    :value="filters.delayed"
                    label="Retrasada"
                    inset
                    @change="updateFilters({ delayed: $event })"
                  ></v-switch>
                </v-col>
                <v-col>
                  <v-switch
                    :value="filters.overworked"
                    label="Con sobreesfuerzo"
                    inset
                    @change="updateFilters({ overworked: $event })"
                  ></v-switch>
                </v-col>
              </v-row>
            </v-tab-item>
            <v-tab-item value="dates">
              <v-row>
                <v-col>
                  <DatePickerInput
                    :value="filters.start_date__gte"
                    label="Fecha inicio planificada (desde)"
                    prepend-icon="mdi-calendar-arrow-right"
                    clearable
                    @input="updateFilters({ start_date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.start_date__lte"
                    label="Fecha inicio planificada (hasta)"
                    prepend-icon="mdi-calendar-arrow-left"
                    clearable
                    @input="updateFilters({ start_date__lte: $event })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <DatePickerInput
                    :value="filters.end_date__gte"
                    label="Fecha límite (desde)"
                    prepend-icon="mdi-calendar-arrow-right"
                    clearable
                    @input="updateFilters({ end_date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.end_date__lte"
                    label="Fecha límite (hasta)"
                    prepend-icon="mdi-calendar-arrow-left"
                    clearable
                    @input="updateFilters({ end_date__lte: $event })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <DatePickerInput
                    :value="filters.current_progress_changed__date__gte"
                    label="Fecha modificación de avance (desde)"
                    prepend-icon="mdi-calendar-arrow-right"
                    clearable
                    @input="updateFilters({ current_progress_changed__date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.current_progress_changed__date__lte"
                    label="Fecha modificación de avance (hasta)"
                    prepend-icon="mdi-calendar-arrow-left"
                    clearable
                    @input="updateFilters({ current_progress_changed__date__lte: $event })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <DatePickerInput
                    :value="filters.validated_changed__date__gte"
                    label="Fecha modificación de validación (desde)"
                    prepend-icon="mdi-calendar-arrow-right"
                    clearable
                    @input="updateFilters({ validated_changed__date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.validated_changed__date__lte"
                    label="Fecha modificación de validación (hasta)"
                    prepend-icon="mdi-calendar-arrow-left"
                    clearable
                    @input="updateFilters({ validated_changed__date__lte: $event })"
                  />
                </v-col>
              </v-row>
            </v-tab-item>
            <v-tab-item value="people">
              <v-row>
                <v-col>
                  <UserAutocomplete
                    :value="developmentUserFilter"
                    label="Desarrollador"
                    prepend-icon="mdi-account"
                    multiple
                    truncate-results
                    clearable
                    @input="updateFilters({ development_user_id__in: $event.join(',') })"
                  />
                </v-col>
                <v-col>
                  <UserAutocomplete
                    :value="validationUserFilter"
                    label="Validador"
                    prepend-icon="mdi-account-check"
                    multiple
                    truncate-results
                    clearable
                    @input="updateFilters({ validation_user_id__in: $event.join(',') })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col cols="6">
                  <UserAutocomplete
                    :value="supportUserFilter"
                    label="Soporte"
                    prepend-icon="mdi-account-question"
                    multiple
                    truncate-results
                    clearable
                    @input="updateFilters({ support_user_id__in: $event.join(',') })"
                  />
                </v-col>
              </v-row>
            </v-tab-item>
          </v-tabs-items>
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
import { mapState, mapActions } from "vuex";
import { range } from "lodash";

import FilterMixin from "@/mixins/filter-mixin";

import EpicService from "@/services/scrum/epic-service";
import SprintService from "@/services/scrum/sprint-service";

export default {
  name: "UserStoryFilters",
  mixins: [FilterMixin],
  data() {
    return {
      epicService: EpicService,
      sprintService: SprintService,
      disableSprintFilter: Boolean(this.filters.sprint_id),
      disableEpicFilter: Boolean(this.filters.epic_id),
      tab: "general",
      priorityOptions: range(1, 11),
      basicFilters: ["search", "status__in", "any_role_user__in"],
    };
  },
  computed: {
    ...mapState("users", {
      userOptions: "users",
    }),
    ...mapState("scrum", {
      riskLevelOptions: "riskLevels",
      userStoryStatusOptions: "userStoryStatus",
      userStoryTypesOptions: "userStoryTypes",
    }),
    statusFilter() {
      return this.splitFilterValue("status__in", true);
    },
    tagFilter() {
      return this.splitFilterValue("tags__name__in");
    },
    anyRoleUserFilter() {
      return this.splitFilterValue("any_role_user__in", true);
    },
    priorityFilter() {
      return this.splitFilterValue("priority__in", true);
    },
    developmentUserFilter() {
      return this.splitFilterValue("development_user_id__in", true);
    },
    validationUserFilter() {
      return this.splitFilterValue("validation_user_id__in", true);
    },
    supportUserFilter() {
      return this.splitFilterValue("support_user_id__in", true);
    },
  },
  created() {
    if (!Object.keys(this.userStoryTypesOptions).length) {
      this.getUserStoryTypes();
    }
  },
  methods: {
    ...mapActions("scrum", ["getUserStoryTypes"]),
  },
};
</script>
