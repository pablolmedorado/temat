<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />

    <v-tabs v-if="id" v-model="tab" class="mb-4" grow show-arrows background-color="transparent">
      <v-tabs-slider />
      <v-tab href="#data">
        <v-icon :small="$vuetify.breakpoint.mdAndUp">mdi-book-account</v-icon>
        <span v-show="$vuetify.breakpoint.mdAndUp" class="ml-2">Información</span>
      </v-tab>
      <v-tab href="#tasks">
        <v-icon :small="$vuetify.breakpoint.mdAndUp">mdi-format-list-checks</v-icon>
        <span v-show="$vuetify.breakpoint.mdAndUp" class="ml-2">Tareas</span>
      </v-tab>
      <v-tab href="#progress">
        <v-icon :small="$vuetify.breakpoint.mdAndUp">mdi-percent</v-icon>
        <span v-show="$vuetify.breakpoint.mdAndUp" class="ml-2">Historial de avance</span>
      </v-tab>
      <v-tab href="#effort">
        <v-icon :small="$vuetify.breakpoint.mdAndUp">mdi-dumbbell</v-icon>
        <span v-show="$vuetify.breakpoint.mdAndUp" class="ml-2">Esfuerzo</span>
      </v-tab>
    </v-tabs>

    <v-tabs-items v-model="tab">
      <v-tab-item value="data">
        <UserStoryData v-if="item" :item.sync="item" @changed:item="showConfirmBeforeLeaving = $event" />
      </v-tab-item>
      <v-tab-item value="tasks">
        <UserStoryTasks v-if="item" :user-story="item" @change:progress="onProgressUpdated" />
      </v-tab-item>
      <v-tab-item value="progress">
        <UserStoryProgress v-if="item" ref="progressComponent" :user-story="item" />
      </v-tab-item>
      <v-tab-item value="effort">
        <UserStoryEffort v-if="item" :user-story="item" @change:effort="onEffortUpdated" />
      </v-tab-item>
    </v-tabs-items>
  </v-container>
</template>

<script>
import { defaultTo } from "lodash";

import UserStoryService from "@/services/scrum/user-story-service";

import ContextBreadcrumbs from "@/components/scrum/ContextBreadcrumbs";
import UserStoryData from "@/components/scrum/tabs/user-stories/UserStoryData";
import UserStoryEffort from "@/components/scrum/tabs/user-stories/UserStoryEffort";
import UserStoryProgress from "@/components/scrum/tabs/user-stories/UserStoryProgress";
import UserStoryTasks from "@/components/scrum/tabs/user-stories/UserStoryTasks";

import useScrumContext, { scrumContextProps } from "@/composables/useScrumContext";
import { handleError } from "@/utils/error-handlers";

const defaultItem = {
  id: null,
  name: "",
  type: null,
  epic: null,
  sprint: null,
  functional_description: "",
  technical_description: "",
  start_date: null,
  end_date: null,
  current_progress: 0,
  current_progress_changed: null,
  validated: null,
  validated_changed: null,
  status: 0,
  planned_effort: 1,
  priority: 10,
  development_user: null,
  development_comments: "",
  validation_user: null,
  validation_comments: "",
  support_user: null,
  support_comments: "",
  cvs_reference: "",
  risk_level: 0,
  risk_comments: "",
  use_migrations: false,
  deployment_notes: "",
  tags: [],
};

export default {
  name: "UserStoryDetail",
  metaInfo() {
    return {
      title: this.id ? "Historia de usuario" : "Nueva historia de usuario",
    };
  },
  components: {
    ContextBreadcrumbs,
    UserStoryData,
    UserStoryTasks,
    UserStoryProgress,
    UserStoryEffort,
  },
  async beforeRouteEnter(to, from, next) {
    try {
      let item;
      if (to.params.id) {
        const response = await UserStoryService.retrieve(to.params.id, { expand: "sprint" });
        item = response.data;
      } else {
        item = {
          ...defaultItem,
          epic: defaultTo(to.query.epic, null),
          sprint: defaultTo(to.query.sprint, null),
        };
      }
      next((vm) => {
        vm.item = item;
        vm.tab = "data";
      });
    } catch (error) {
      handleError(error);
      if (from.name === null) {
        next({ name: "user-stories" });
      }
    }
  },
  async beforeRouteUpdate(to, from, next) {
    this.item = null;
    try {
      if (to.params.id) {
        await this.fetchItem(to.params.id);
      } else {
        this.item = {
          ...defaultItem,
          epic: defaultTo(to.query.epic, null),
          sprint: defaultTo(to.query.sprint, null),
        };
      }
      this.tab = "data";
      next();
    } catch (error) {
      handleError(error);
      next({ name: "user-stories" });
    }
  },
  beforeRouteLeave(to, from, next) {
    if (!this.showConfirmBeforeLeaving || confirm("Hay cambios sin guardar, ¿estás seguro que deseas salir?")) {
      next();
    }
  },
  props: {
    id: {
      type: String,
      default: undefined,
    },
    ...scrumContextProps,
  },
  setup(props) {
    const { contextItem } = useScrumContext(props);
    return {
      contextItem,
    };
  },
  data() {
    return {
      item: null,
      tab: "data",
      showConfirmBeforeLeaving: false,
    };
  },
  computed: {
    breadcrumbs() {
      const currentItemBreadcrumb = {
        text: (this.item && this.item.name) || "Nueva historia de usuario",
        disabled: true,
      };
      if (this.contextItem) {
        let result = [];
        const contextItemBreadcrumb = { text: this.contextItem.name, disabled: false, link: false };
        if (this.sprintId) {
          result = [
            {
              text: "Sprints",
              to: { name: "sprints" },
              exact: true,
            },
            contextItemBreadcrumb,
            {
              text: "Historias de usuario",
              to: { name: "sprint-user-stories", params: { sprintId: this.sprintId } },
              exact: true,
            },
            currentItemBreadcrumb,
          ];
        }
        if (this.epicId) {
          result = [
            {
              text: "Épicas",
              to: { name: "epics" },
              exact: true,
            },
            contextItemBreadcrumb,
            {
              text: "Historias de usuario",
              to: { name: "epic-user-stories", params: { epicId: this.epicId } },
              exact: true,
            },
            currentItemBreadcrumb,
          ];
        }
        return result;
      } else {
        return [
          {
            text: "Historias de usuario",
            to: { name: "user-stories" },
            exact: true,
          },
          currentItemBreadcrumb,
        ];
      }
    },
  },
  watch: {
    tab(newValue, oldValue) {
      if (oldValue === "data" && this.showConfirmBeforeLeaving) {
        alert("Hay cambios sin guardar en el formulario que podrían perderse al interactuar con otras pestañas.");
      }
    },
  },
  methods: {
    async fetchItem(id) {
      const response = await UserStoryService.retrieve(id, { expand: "sprint" });
      this.item = response.data;
    },
    onProgressUpdated() {
      this.fetchItem(this.id);
      if (this.$refs.progressComponent) {
        this.$refs.progressComponent.fetchItems();
      }
    },
    onEffortUpdated() {
      this.fetchItem(this.id);
    },
  },
};
</script>

<style scoped>
::v-deep .v-tabs-items {
  background-color: transparent !important;
}
::v-deep .v-window {
  overflow: visible;
}
</style>
