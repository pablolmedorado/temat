<template>
  <v-container fluid>
    <ContextBreadcrumbs v-if="hasContext" :items="breadcrumbs" />
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :local-storage-namespace="localStorageNamespace"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :system-filters="systemFilters"
          :quick-filters="quickFilters"
          :default-quick-filter="defaultQuickFilter"
          :allow-add="modelClass.ADD_PERMISSION"
          :allow-delete="modelClass.DELETE_PERMISSION"
          :disable-row-edition="isLoading"
          :selectable-rows="userHasPermission(modelClass.CHANGE_PERMISSION)"
          custom-headers
          delete-child-items-warning
        >
          <template v-if="userHasPermission(modelClass.CHANGE_PERMISSION)" #toolbar="{ selectedItems, isIndexLoading }">
            <v-tooltip bottom>
              <template #activator="{ attrs, on }">
                <v-btn
                  icon
                  :disabled="!selectedItems.length || isIndexLoading"
                  v-bind="attrs"
                  v-on="on"
                  @click="$refs.bulkUpdateDialog.open(selectedItems)"
                >
                  <v-badge :value="selectedItems.length" :content="`${selectedItems.length}`" color="secondary" overlap>
                    <v-icon>mdi-playlist-edit</v-icon>
                  </v-badge>
                </v-btn>
              </template>
              <span>Actualización en bloque</span>
            </v-tooltip>
            <v-divider class="mx-2" vertical inset />
          </template>

          <template #item.name="{ value }">
            <TruncatedText :value="value" :text-length="100" />
          </template>
          <template #item.planned_effort="{ value }">{{ value }} UT</template>
          <template #item.start_date="{ value }">
            <DateRouterLink v-if="value" :date="value" />
          </template>
          <template #item.end_date="{ value }">
            <DateRouterLink v-if="value" :date="value" />
          </template>
          <template #item.priority="{ value }">
            <v-icon>{{ `mdi-numeric-${value}-box` }}</v-icon>
          </template>
          <template #item.status="{ item }">
            <UserStoryIndexStatus :user-story="item" />
          </template>
          <template #item.people="{ item }">
            <UserStoryActors :user-story="item" :avatar-size="32" />
          </template>
          <template #item.tags="{ value }">
            <TagLabels v-if="value" :tags="value" small @click:tag="setTagFilter" />
          </template>
          <template #item.table_actions="{ item }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon :to="buildDetailLink(item.id)" v-bind="attrs" v-on="on">
                  <v-icon>mdi-open-in-app</v-icon>
                </v-btn>
              </template>
              <span> Ver detalle </span>
            </v-tooltip>
            <v-tooltip v-if="item.status < 3 && canDevelop(item)" bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" :disabled="isLoading" @click.stop="$refs.taskDialog.open(item)" v-on="on">
                  <v-icon>mdi-format-list-checks</v-icon>
                </v-btn>
              </template>
              <span> Ver tareas </span>
            </v-tooltip>
            <v-tooltip v-if="item.status < 4" bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" :disabled="isLoading" @click.stop="openNewEffortDialog(item)" v-on="on">
                  <v-icon>mdi-dumbbell</v-icon>
                </v-btn>
              </template>
              <span> Añadir esfuerzo </span>
            </v-tooltip>
            <v-tooltip v-if="item.status === 3 && canValidate(item)" bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  v-bind="attrs"
                  :disabled="isLoading"
                  :loading="isTaskLoading('validate-item', item.id)"
                  @click="validateItem(item)"
                  v-on="on"
                >
                  <v-icon>mdi-check-bold</v-icon>
                </v-btn>
              </template>
              <span> Validar </span>
            </v-tooltip>
          </template>

          <template #fab="{ canAddItems }">
            <v-btn v-if="canAddItems()" fab fixed bottom right color="secondary" :to="newUserStoryRouteConfig">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <TaskQuickManagementDialog ref="taskDialog" @updated-tasks="fetchTableItems" />

    <FormDialog ref="effortFormDialog" verbose-name="esfuerzo" :form-component="effortFormComponent" />

    <UserStoryBulkUpdateDialog ref="bulkUpdateDialog" @change:user-stories="fetchTableItems" />
  </v-container>
</template>

<script>
import { mapState } from "pinia";
import { get } from "lodash";

import Effort from "@/modules/scrum/models/effort";
import UserStory from "@/modules/scrum/models/user-story";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import EffortForm from "@/modules/scrum/components/forms/EffortForm";
import TaskQuickManagementDialog from "@/modules/scrum/components/dialogs/TaskQuickManagementDialog";
import UserStoryActors from "@/modules/scrum/components/UserStoryActors";
import UserStoryBulkUpdateDialog from "@/modules/scrum/components/dialogs/UserStoryBulkUpdateDialog";
import UserStoryFilters from "@/modules/scrum/components/filters/UserStoryFilters";
import UserStoryIndexStatus from "@/modules/scrum/components/UserStoryIndexStatus";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import useScrumContext, { scrumContextProps } from "@/modules/scrum/composables/useScrumContext";
import { getServiceByBasename } from "@/services";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "UserStoryListView",
  metaInfo() {
    let title = "Historias de usuario";
    if (this.hasContext) {
      const model = this.sprintId ? "Sprint" : "Épica";
      title = `${get(this.contextItem, "name", model)} - Historias de usuario`;
    }
    return { title };
  },
  components: {
    ContextBreadcrumbs,
    TaskQuickManagementDialog,
    UserStoryActors,
    UserStoryBulkUpdateDialog,
    UserStoryIndexStatus,
  },
  props: {
    ...scrumContextProps,
  },
  setup(props) {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });
    const { hasContext, contextItem } = useScrumContext(props);
    return {
      isLoading,
      isTaskLoading,
      addTask,
      removeTask,
      hasContext,
      contextItem,
    };
  },
  data() {
    return {
      modelClass: UserStory,
      service: getServiceByBasename(UserStory.serviceBasename),
      tableHeaders: [
        { text: "Id", align: "start", sortable: false, value: "id" },
        { text: "Título", align: "start", sortable: true, value: "name", fixed: true },
        { text: "Tipo", align: "start", sortable: true, value: "type.name", sortingField: "type__name" },
        { text: "Épica", align: "start", sortable: true, value: "epic.name", sortingField: "epic__name" },
        {
          text: "Sprint",
          align: "start",
          sortable: true,
          value: "sprint.name",
          sortingField: "sprint__name",
          default: true,
        },
        { text: "Esfuerzo p.", align: "start", sortable: true, value: "planned_effort" },
        { text: "Fecha inicio p.", align: "start", sortable: true, value: "start_date" },
        { text: "Fecha límite", align: "start", sortable: true, value: "end_date", default: true },
        { text: "Prioridad", align: "start", sortable: true, value: "priority", default: true },
        { text: "Referencia SCV", align: "start", sortable: true, value: "cvs_reference" },
        {
          text: "Estado",
          align: "start",
          sortable: true,
          value: "status",
          fields: ["status", "current_progress", "validated", "risk_level"],
          orderingField: "current_progress",
          fixed: true,
        },
        {
          text: "Personas",
          align: "start",
          sortable: false,
          value: "people",
          fields: ["development_user", "validation_user", "support_user"],
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
      ],
      tableOptions: {
        sortBy: ["end_date", "priority"],
        sortDesc: [false, false],
        multiSort: true,
      },
      filterComponent: UserStoryFilters,
      effortFormComponent: EffortForm,
      showTaskDialog: false,
    };
  },
  computed: {
    ...mapState(useMainStore, ["loggedUser"]),
    breadcrumbs() {
      if (this.contextItem) {
        const result = [
          { text: this.contextItem.name, disabled: false, link: false },
          { text: "Historias de usuario", disabled: true },
        ];
        if (this.sprintId) {
          result.unshift({
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          });
        }
        if (this.epicId) {
          result.unshift({
            text: "Épicas",
            to: { name: "epics" },
            exact: true,
          });
        }
        return result;
      } else {
        return [];
      }
    },
    localStorageNamespace() {
      let namespace = UserStory.localStorageNamespace;
      if (this.sprintId) {
        namespace += "Sprint";
      }
      if (this.epicId) {
        namespace += "Epic";
      }
      return namespace;
    },
    newUserStoryRouteConfig() {
      const queryParams = {};
      if (this.sprintId) {
        queryParams.sprint = this.sprintId;
      }
      if (this.epicId) {
        queryParams.epic = this.epicId;
      }
      return { name: "user-story-new", query: queryParams };
    },
    systemFilters() {
      const filters = {};
      if (this.sprintId) {
        filters.sprint_id = this.sprintId;
      }
      if (this.epicId) {
        filters.epic_id = this.epicId;
      }
      return filters;
    },
    quickFilters() {
      return [
        {
          key: "all",
          label: "Todas las historias",
          filters: {},
        },
        {
          key: "ongoing",
          label: "Historias en curso",
          filters: {
            status__in: "1,2,3",
          },
        },
        {
          key: "my-stories",
          label: "Mis historias en curso",
          filters: {
            status__in: "1,2,3",
            any_role_user__in: String(this.loggedUser.id),
          },
        },
        {
          key: "my-pending-developments",
          label: "Mis desarrollos pendientes",
          filters: {
            status__in: "1,2",
            development_user_id__in: String(this.loggedUser.id),
          },
        },
        {
          key: "my-pending-validations",
          label: "Mis validaciones pendientes",
          filters: {
            status__in: "3",
            validation_user_id__in: String(this.loggedUser.id),
          },
        },
      ];
    },
    defaultQuickFilter() {
      if (this.hasContext) {
        return "all";
      } else {
        return userHasPermission(this.modelClass.VIEW_PERMISSION) ? "ongoing" : "my-stories";
      }
    },
  },
  watch: {
    tableHeaders(newValue) {
      const sortingValues = newValue.map((header) => header.sortingField || header.value);
      if (this.tableOptions.sortBy.some((header) => !sortingValues.includes(header))) {
        this.tableOptions = {
          ...this.tableOptions,
          sortBy: [],
          sortDesc: [],
        };
      }
    },
  },
  methods: {
    userHasPermission,
    fetchTableItems() {
      this.$refs.itemIndex.fetchTableItems();
    },
    buildDetailLink(id) {
      const linkConfig = { name: "user-story", params: { id } };
      if (this.sprintId) {
        linkConfig.name = "sprint-user-story";
        linkConfig.params.sprintId = this.sprintId;
      }
      if (this.epicId) {
        linkConfig.name = "epic-user-story";
        linkConfig.params.epicId = this.epicId;
      }
      return linkConfig;
    },
    canDevelop(item) {
      return this.loggedUser.id === item.development_user || userHasPermission(this.modelClass.CHANGE_PERMISSION);
    },
    canValidate(item) {
      return this.loggedUser.id === item.validation_user || userHasPermission(this.modelClass.CHANGE_PERMISSION);
    },
    async validateItem(item) {
      if (confirm(`Estás seguro de que deseas validar la historia "${item.name}"`)) {
        this.addTask("validate-item", item.id);
        try {
          await this.service.validate(item.id);
          this.$refs.itemIndex.fetchTableItems();
        } finally {
          this.removeTask("validate-item", item.id);
        }
      }
    },
    calculateLoggedUserRole(userStory) {
      switch (this.loggedUser.id) {
        case userStory.development_user:
          return "D";
        case userStory.validation_user:
          return "V";
        case userStory.support_user:
          return "S";
        default:
          return null;
      }
    },
    openNewEffortDialog(userStory) {
      this.$refs.effortFormDialog.open({
        ...Effort.defaults,
        role: this.calculateLoggedUserRole(userStory),
        user_story: userStory.id,
      });
    },
    setTagFilter(tag) {
      this.$refs.itemIndex.addFilter({ tags__name__in: tag });
      this.$nextTick(() => {
        this.$refs.itemIndex.fetchTableItems();
      });
    },
  },
};
</script>
