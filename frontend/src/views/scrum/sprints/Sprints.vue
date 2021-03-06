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
import { mapState } from "vuex";

import Sprint from "@/models/scrum/sprint";

import SprintFilters from "@/components/scrum/filters/SprintFilters";
import SprintForm from "@/components/scrum/forms/SprintForm";
import SprintViewSelector from "@/components/scrum/SprintViewSelector";

export default {
  name: "Sprints",
  metaInfo: {
    title: "Sprints",
  },
  components: { SprintViewSelector },
  data() {
    return {
      modelClass: Sprint,
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
      filterComponent: SprintFilters,
      quickFilters: [{ key: "ongoing", label: "En curso", filters: { ongoing: true } }],
      formComponent: SprintForm,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
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

<style scoped>
::v-deep .v-progress-circular__info {
  font-size: 0.79rem;
}
</style>
