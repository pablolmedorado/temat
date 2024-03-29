<template>
  <div>
    <v-row>
      <v-col lg="3" sm="6" cols="12">
        <v-text-field
          :value="filters.search"
          label="Buscar"
          placeholder="Id, nombre, descripciones, comentarios, notas, scv..."
          prepend-icon="mdi-magnify"
          clearable
          @input="updateFilters({ search: $event })"
          @keyup.enter="$emit('apply:filters')"
        />
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
        <v-btn class="my-2" color="primary" :disabled="disabled" @click="$emit('apply:filters')"> Filtrar </v-btn>
      </v-col>
    </v-row>

    <v-dialog
      ref="advancedFiltersDialog"
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
          <v-tabs v-model="tab" class="mb-4">
            <v-tab href="#general">General</v-tab>
            <v-tab href="#status">Estado</v-tab>
            <v-tab href="#dates">Fechas</v-tab>
            <v-tab href="#people">Personas</v-tab>
            <v-tab href="#others">Otros</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item value="general">
              <v-row>
                <v-col>
                  <v-text-field
                    :value="filters.search"
                    label="Buscar"
                    placeholder="Id, nombre, descripciones, comentarios, notas, scv..."
                    prepend-icon="mdi-magnify"
                    clearable
                    @input="updateFilters({ search: $event })"
                  />
                </v-col>
              </v-row>
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
                  />
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
                  />
                </v-col>
              </v-row>
              <v-row v-if="!context.sprint">
                <v-col>
                  <AsyncAutocomplete
                    :value="filters.sprint_id"
                    :service="sprintService"
                    search-field="name"
                    search-lookup="icontains"
                    label="Sprint"
                    prepend-icon="mdi-run-fast"
                    @input="updateFilters({ sprint_id: $event })"
                  />
                </v-col>
              </v-row>
              <v-row v-if="!context.epic">
                <v-col>
                  <AsyncAutocomplete
                    :value="filters.epic_id"
                    :service="epicService"
                    search-field="name"
                    search-lookup="icontains"
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
            </v-tab-item>
            <v-tab-item value="status">
              <v-row>
                <v-col>
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
                      <span v-if="index === 1" class="grey--text text-caption">
                        (+{{ statusFilter.length - 1 }} más)
                      </span>
                    </template>
                  </v-select>
                </v-col>
              </v-row>
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
                  />
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
                  />
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
                  />
                </v-col>
                <v-col>
                  <v-switch
                    class="pl-1"
                    :value="filters.validated"
                    true-value="false"
                    false-value=""
                    label="Validación rechazada"
                    inset
                    @change="updateFilters({ validated: $event })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-switch
                    class="pl-1"
                    :value="filters.delayed"
                    label="Retrasada"
                    inset
                    @change="updateFilters({ delayed: $event })"
                  />
                </v-col>
                <v-col>
                  <v-switch
                    class="pl-1"
                    :value="filters.overworked"
                    label="Con sobreesfuerzo"
                    inset
                    @change="updateFilters({ overworked: $event })"
                  />
                </v-col>
              </v-row>
            </v-tab-item>
            <v-tab-item value="dates">
              <v-row>
                <v-col>
                  <DatePickerInput
                    :value="filters.start_date__gte"
                    label="Fecha inicio planificada (desde)"
                    prepend-icon="mdi-calendar-start"
                    clearable
                    @input="updateFilters({ start_date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.start_date__lte"
                    label="Fecha inicio planificada (hasta)"
                    prepend-icon="mdi-calendar-end"
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
                    prepend-icon="mdi-calendar-start"
                    clearable
                    @input="updateFilters({ end_date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.end_date__lte"
                    label="Fecha límite (hasta)"
                    prepend-icon="mdi-calendar-end"
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
                    prepend-icon="mdi-calendar-start"
                    clearable
                    @input="updateFilters({ current_progress_changed__date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.current_progress_changed__date__lte"
                    label="Fecha modificación de avance (hasta)"
                    prepend-icon="mdi-calendar-end"
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
                    prepend-icon="mdi-calendar-start"
                    clearable
                    @input="updateFilters({ validated_changed__date__gte: $event })"
                  />
                </v-col>
                <v-col>
                  <DatePickerInput
                    :value="filters.validated_changed__date__lte"
                    label="Fecha modificación de validación (hasta)"
                    prepend-icon="mdi-calendar-end"
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
                    :value="anyRoleUserFilter"
                    label="Usuario (cualquier rol)"
                    prepend-icon="mdi-account-multiple"
                    multiple
                    truncate-results
                    clearable
                    @input="updateFilters({ any_role_user__in: $event.join(',') })"
                  />
                </v-col>
              </v-row>
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
            <v-tab-item value="others">
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
                  />
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
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-text-field
                    :value="filters.cvs_issue_id"
                    label="Issue SCV"
                    type="number"
                    min="0"
                    prepend-icon="mdi-record-circle-outline"
                    clearable
                    @input="updateFilters({ cvs_issue_id: $event })"
                  />
                </v-col>
                <v-col>
                  <v-text-field
                    :value="filters.cvs_pull_request_id"
                    label="Pull Request SCV"
                    type="number"
                    min="0"
                    prepend-icon="mdi-source-pull"
                    clearable
                    @input="updateFilters({ cvs_pull_request_id: $event })"
                  />
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <v-switch
                    class="pl-1"
                    :value="filters.use_migrations"
                    label="Usa migraciones"
                    inset
                    @change="updateFilters({ use_migrations: $event })"
                  />
                </v-col>
              </v-row>
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-btn color="warning" text @click="clearFilters">Limpiar</v-btn>
          <v-spacer />
          <v-btn text @click="closeFiltersDialog"> Volver </v-btn>
          <v-btn text :disabled="disabled" @click="applyFiltersFromDialog"> Filtrar </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { computed, inject, ref, toRefs } from "@vue/composition-api";
import { range } from "lodash-es";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import EpicService from "@/modules/scrum/services/epic-service";
import SprintService from "@/modules/scrum/services/sprint-service";

import { useFilters, filterProps } from "@/composables/filters";
import { useUserStoryTypes } from "@/modules/scrum/composables/user-story-types";

export default {
  name: "UserStoryFilters",
  props: filterProps,
  setup() {
    // Store
    const userStoryStore = useUserStoryStore();

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
    } = useFilters({ basicFilters: ["search", "status__in", "any_role_user__in"] });
    const { userStoryTypes: userStoryTypesOptions } = useUserStoryTypes();

    // State
    const epicService = EpicService;
    const sprintService = SprintService;
    const tab = ref("general");
    const priorityOptions = range(1, 11);

    // Computed
    const { riskLevels: riskLevelOptions, userStoryStatus: userStoryStatusOptions } = toRefs(userStoryStore);
    const statusFilter = computed(() => splitFilterValue("status__in", true));
    const tagFilter = computed(() => splitFilterValue("tags__name__in"));
    const anyRoleUserFilter = computed(() => splitFilterValue("any_role_user__in", true));
    const priorityFilter = computed(() => splitFilterValue("priority__in", true));
    const developmentUserFilter = computed(() => splitFilterValue("development_user_id__in", true));
    const validationUserFilter = computed(() => splitFilterValue("validation_user_id__in", true));
    const supportUserFilter = computed(() => splitFilterValue("support_user_id__in", true));

    // Dependency injection
    const context = inject("context", {});

    return {
      // Injections
      context,
      // State
      showFiltersDialog,
      hasAdvancedFilters,
      userStoryTypesOptions,
      epicService,
      sprintService,
      tab,
      priorityOptions,
      // Computed
      riskLevelOptions,
      userStoryStatusOptions,
      statusFilter,
      tagFilter,
      anyRoleUserFilter,
      priorityFilter,
      developmentUserFilter,
      validationUserFilter,
      supportUserFilter,
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
