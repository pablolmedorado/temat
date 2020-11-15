<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-key="sprint"
          verbose-name="Sprint"
          verbose-name-plural="Sprints"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :quick-filters="quickFilters"
          :service="service"
          :form-component="formComponent"
          :default-item="defaultItem"
          custom-headers
          advanced-filters
          delete-child-items-warning
        >
          <template #item.name="{ value }">
            <TruncatedText :value="value" :text-length="100" />
          </template>
          <template #item.start_date="{ value }">
            <DateRouterLink :date="value"></DateRouterLink>
          </template>
          <template #item.end_date="{ value }">
            <DateRouterLink :date="value"></DateRouterLink>
          </template>
          <template #item.ongoing="{ item }">
            <v-simple-checkbox v-model="item.ongoing" disabled></v-simple-checkbox>
          </template>
          <template #item.accountable_user="{ value }">
            <UserPill :user="value"></UserPill>
          </template>
          <template #item.current_progress="{ value }">
            <v-progress-circular :rotate="-90" :size="32" :value="value" :width="3" color="primary">
              {{ value }}
            </v-progress-circular>
          </template>
          <template #item.tags="{ value }">
            <TagLabels v-if="value" :tags="value" @click:tag="setTagFilter" />
          </template>
          <template #item.table_actions="{ item }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :to="{ name: 'sprint-user-stories', params: { sprintId: item.id } }"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon>mdi-book-account</v-icon>
                </v-btn>
              </template>
              <span>
                Ver historias de usuario asociadas
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon :to="{ name: 'sprint-kanban', params: { sprintId: item.id } }" v-bind="attrs" v-on="on">
                  <v-icon>mdi-teach</v-icon>
                </v-btn>
              </template>
              <span>
                Kanban
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon :to="{ name: 'sprint-chart', params: { sprintId: item.id } }" v-bind="attrs" v-on="on">
                  <v-icon>mdi-fire</v-icon>
                </v-btn>
              </template>
              <span>
                Diagrama de quemado (Burn-down/up)
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon :to="{ name: 'sprint-gantt', params: { sprintId: item.id } }" v-bind="attrs" v-on="on">
                  <v-icon>mdi-chart-timeline</v-icon>
                </v-btn>
              </template>
              <span>
                Diagrama de Gantt
              </span>
            </v-tooltip>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import { DateTime } from "luxon";

import SprintService from "@/services/scrum/sprint-service";

import SprintFilters from "@/components/scrum/filters/SprintFilters";
import SprintForm from "@/components/scrum/forms/SprintForm";

export default {
  name: "Sprints",
  metaInfo: {
    title: "Sprints",
  },
  data() {
    return {
      tableHeaders: [
        { text: "Nombre", align: "start", sortable: true, value: "name", fixed: true },
        { text: "Fecha inicio", align: "start", sortable: true, value: "start_date", default: true },
        { text: "Fecha fin", align: "start", sortable: true, value: "end_date", default: true },
        {
          text: "En curso",
          align: "start",
          sortable: true,
          value: "ongoing",
          sortingField: "annotated_ongoing",
          default: true,
        },
        {
          text: "Usuario responsable",
          align: "start",
          sortable: true,
          value: "accountable_user",
          sortingField: "accountable_user__acronym",
          default: true,
        },
        {
          text: "Historias de usuario",
          align: "start",
          sortable: true,
          sortingField: "user_stories__count",
          value: "num_of_user_stories",
        },
        {
          text: "Progreso",
          align: "start",
          sortable: true,
          sortingField: "annotated_current_progress",
          value: "current_progress",
        },
        { text: "Tags", align: "start", sortable: false, value: "tags" },
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
      ],
      tableOptions: {
        sortBy: ["ongoing", "start_date"],
        sortDesc: [true, true],
        multiSort: true,
      },
      service: SprintService,
      filterComponent: SprintFilters,
      quickFilters: [{ label: "En curso", filters: { ongoing: true }, default: true }],
      formComponent: SprintForm,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    defaultItem() {
      return {
        id: null,
        start_date: DateTime.local().toISODate(),
        end_date: null,
        accountable_user: null,
        tags: [],
      };
    },
  },
  methods: {
    setTagFilter(tag) {
      this.$refs.itemIndex.addFilter({ tags__name__in: tag });
      this.$nextTick(() => {
        this.$refs.itemIndex.fetchTableItems();
      });
    },
  },
};
</script>
