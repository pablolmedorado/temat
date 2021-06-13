<template>
  <v-container fluid>
    <ContextBreadcrumbs v-if="hasContext" :items="breadcrumbs" />
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-namespace="userStory"
          verbose-name="Historia de usuario"
          verbose-name-plural="Historias de usuario"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :system-filters="systemFilters"
          :quick-filters="quickFilters"
          :default-quick-filter="defaultQuickFilter"
          :service="service"
          :can-create="() => userHasPermission('scrum.add_userstory')"
          :can-edit="() => false"
          :can-delete="() => userHasPermission('scrum.delete_userstory')"
          :disable-row-edition="isLoading"
          custom-headers
          advanced-filters
          delete-child-items-warning
        >
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
            <TagLabels v-if="value" :tags="value" @click:tag="setTagFilter" />
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

          <template #fab>
            <v-btn
              v-if="userHasPermission('scrum.add_userstory')"
              fab
              fixed
              bottom
              right
              color="secondary"
              :to="newUserStoryRouteConfig"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <TaskQuickManagementDialog ref="taskDialog" @updated-tasks="fetchTableItems" />

    <FormDialog ref="effortFormDialog" verbose-name="esfuerzo" :form-component="effortFormComponent" />
  </v-container>
</template>

<script>
import { mapState } from "vuex";
import { DateTime } from "luxon";

import UserStoryService from "@/services/scrum/user-story-service";

import ContextBreadcrumbs from "@/components/scrum/ContextBreadcrumbs";
import EffortForm from "@/components/scrum/forms/EffortForm";
import TaskQuickManagementDialog from "@/components/scrum/dialogs/TaskQuickManagementDialog";
import UserStoryActors from "@/components/scrum/UserStoryActors";
import UserStoryFilters from "@/components/scrum/filters/UserStoryFilters";
import UserStoryIndexStatus from "@/components/scrum/UserStoryIndexStatus";

import useLoading from "@/composables/useLoading";
import useScrumContext, { scrumContextProps } from "@/composables/useScrumContext";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "UserStories",
  metaInfo() {
    let title = "Historias de usuario";
    if (this.hasContext) {
      const model = this.sprintId ? "Sprint" : "Épica";
      title = `${model} - historias de usuario`;
    }
    return { title };
  },
  components: {
    ContextBreadcrumbs,
    TaskQuickManagementDialog,
    UserStoryActors,
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
        { text: "Tags", align: "start", sortable: false, value: "tags" },
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
      ],
      tableOptions: {
        sortBy: ["end_date", "priority"],
        sortDesc: [false, false],
        multiSort: true,
      },
      service: UserStoryService,
      filterComponent: UserStoryFilters,
      effortFormComponent: EffortForm,
      showTaskDialog: false,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
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
        return null;
      } else {
        return userHasPermission("scrum.view_userstory") ? "ongoing" : "my-stories";
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
      return this.loggedUser.id === item.development_user || userHasPermission("scrum.change_userstory");
    },
    canValidate(item) {
      return this.loggedUser.id === item.validation_user || userHasPermission("scrum.change_userstory");
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
        id: null,
        date: DateTime.local().toISODate(),
        user: this.loggedUser.id,
        role: this.calculateLoggedUserRole(userStory),
        user_story: userStory.id,
        effort: 1,
        comments: "",
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
