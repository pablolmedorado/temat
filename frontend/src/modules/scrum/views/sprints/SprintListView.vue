<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :quick-filters="quickFilters"
          default-quick-filter="ongoing"
          :form-component="formComponent"
          :allow-add="modelClass.ADD_PERMISSION"
          :allow-change="modelClass.CHANGE_PERMISSION"
          :allow-delete="modelClass.DELETE_PERMISSION"
          custom-headers
          delete-child-items-warning
        >
          <template #item.name="{ value }">
            <TruncatedText :value="value" :text-length="100" />
          </template>
          <template #item.start_date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.end_date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.ongoing="{ item }">
            <v-simple-checkbox v-model="item.ongoing" disabled />
          </template>
          <template #item.accountable_user="{ value }">
            <UserPill :user="value" />
          </template>
          <template #item.effort="{ item }">{{ item.current_effort }}/{{ item.planned_effort }} UT</template>
          <template #item.current_progress="{ value }">
            <v-progress-circular :rotate="-90" :size="32" :value="value" :width="3" color="primary">
              {{ value }}
            </v-progress-circular>
          </template>
          <template #item.tags="{ value }">
            <TagLabels v-if="value" :tags="value" small @click:tag="setTagFilter" />
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
              <span> Ver historias de usuario asociadas </span>
            </v-tooltip>
            <SprintViewSelector :sprint-id="item.id" menu />
          </template>
        </ItemIndex>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { nextTick } from "@vue/composition-api";

import Sprint from "@/modules/scrum/models/sprint";

import SprintFilters from "@/modules/scrum/components/filters/SprintFilters";
import SprintForm from "@/modules/scrum/components/forms/SprintForm";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

export default {
  name: "SprintListView",
  metaInfo: {
    title: "Sprints",
  },
  components: { SprintViewSelector },
  setup(props, { refs }) {
    // State
    const modelClass = Sprint;
    const tableHeaders = [
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
        text: "Esfuerzo",
        align: "start",
        sortable: true,
        sortingField: "annotated_current_effort",
        value: "effort",
        fields: ["planned_effort", "current_effort"],
      },
      {
        text: "Progreso",
        align: "start",
        sortable: true,
        sortingField: "annotated_current_progress",
        value: "current_progress",
      },
      {
        text: "Tags",
        align: "start",
        sortable: false,
        value: "tags",
        fields: ["tags.name", "tags.colour", "tags.icon"],
      },
      { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
    ];
    const tableOptions = {
      sortBy: ["ongoing", "start_date"],
      sortDesc: [true, true],
      multiSort: true,
    };
    const filterComponent = SprintFilters;
    const quickFilters = [{ key: "ongoing", label: "En curso", filters: { ongoing: true } }];
    const formComponent = SprintForm;

    // Methods
    function setTagFilter(tag) {
      refs.itemIndex.addFilter({ tags__name__in: tag });
      nextTick(() => {
        refs.itemIndex.fetchTableItems();
      });
    }

    return {
      // State
      modelClass,
      tableHeaders,
      tableOptions,
      filterComponent,
      quickFilters,
      formComponent,
      // Methods
      setTagFilter,
    };
  },
};
</script>

<style scoped>
::v-deep .v-progress-circular__info {
  font-size: 0.79rem;
}
</style>
