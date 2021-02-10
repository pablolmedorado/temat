<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-key="epic"
          verbose-name="Épica"
          verbose-name-plural="Épicas"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :quick-filters="quickFilters"
          default-quick-filter="ongoing"
          :service="service"
          :form-component="formComponent"
          :default-item="defaultItem"
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
import { mapState } from "vuex";
import { isWebUri } from "valid-url";

import EpicService from "@/services/scrum/epic-service";

import EpicFilters from "@/components/scrum/filters/EpicFilters";
import EpicForm from "@/components/scrum/forms/EpicForm";

export default {
  name: "Epics",
  metaInfo: {
    title: "Épicas",
  },
  data() {
    return {
      tableHeaders: [
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
          text: "Progreso",
          align: "start",
          sortable: true,
          sortingField: "annotated_current_progress",
          value: "current_progress",
          default: true,
        },
        { text: "Tags", align: "start", sortable: false, value: "tags" },
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
      ],
      tableOptions: {
        sortBy: ["name"],
        sortDesc: [false],
        mustSort: true,
      },
      service: EpicService,
      filterComponent: EpicFilters,
      quickFilters: [{ key: "ongoing", label: "En curso", filters: { finished: false } }],
      formComponent: EpicForm,
      defaultItem: {
        id: null,
        name: "",
        description: "",
        external_reference: "",
        tags: [],
      },
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
  },
  methods: {
    isWebUri,
    setTagFilter(tag) {
      this.$refs.itemIndex.addFilter({ tags__name__in: tag });
      this.$nextTick(() => {
        this.$refs.itemIndex.fetchTableItems();
      });
    },
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
