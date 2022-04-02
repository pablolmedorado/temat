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
          <template #item.description="{ value }">
            <TruncatedText :value="value" :text-length="100" />
          </template>
          <template #item.external_reference="{ value }">
            <a v-if="isWebUri(value)" :href="value" target="_blank">
              <v-icon>mdi-open-in-new</v-icon>
            </a>
            <template v-else>
              <TruncatedText :value="value" :text-length="100" />
            </template>
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
                <v-btn icon :to="{ name: 'epic-user-stories', params: { epicId: item.id } }" v-bind="attrs" v-on="on">
                  <v-icon>mdi-book-account</v-icon>
                </v-btn>
              </template>
              <span> Ver historias de usuario asociadas </span>
            </v-tooltip>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { nextTick } from "@vue/composition-api";
import { isWebUri } from "valid-url";

import Epic from "@/modules/scrum/models/epic";

import EpicFilters from "@/modules/scrum/components/filters/EpicFilters";
import EpicForm from "@/modules/scrum/components/forms/EpicForm";

export default {
  name: "EpicListView",
  metaInfo: {
    title: "Épicas",
  },
  setup(props, { refs }) {
    // State
    const modelClass = Epic;
    const tableHeaders = [
      { text: "Nombre", align: "start", sortable: true, value: "name", fixed: true },
      { text: "Descripción", align: "start", sortable: false, value: "description", default: true },
      { text: "Referencia externa", align: "start", sortable: false, value: "external_reference", default: true },
      {
        text: "Historias de usuario",
        align: "start",
        sortable: true,
        sortingField: "user_stories__count",
        value: "num_of_user_stories",
        default: true,
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
        default: true,
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
      sortBy: ["name"],
      sortDesc: [false],
      mustSort: true,
    };
    const filterComponent = EpicFilters;
    const quickFilters = [{ key: "ongoing", label: "En curso", filters: { finished: false } }];
    const formComponent = EpicForm;

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
      isWebUri,
      setTagFilter,
    };
  },
};
</script>

<style scoped>
a {
  text-decoration: none;
}
::v-deep .v-progress-circular__info {
  font-size: 0.79rem;
}
</style>
