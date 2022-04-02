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
import { computed, ref, watch } from "@vue/composition-api";
import { defaultTo, invoke } from "lodash-es";

import UserStory from "@/modules/scrum/models/user-story";

import UserStoryService from "@/modules/scrum/services/user-story-service";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import UserStoryData from "@/modules/scrum/components/tabs/user-stories/UserStoryData";
import UserStoryEffort from "@/modules/scrum/components/tabs/user-stories/UserStoryEffort";
import UserStoryProgress from "@/modules/scrum/components/tabs/user-stories/UserStoryProgress";
import UserStoryTasks from "@/modules/scrum/components/tabs/user-stories/UserStoryTasks";

import useScrumContext, { scrumContextProps } from "@/modules/scrum/composables/useScrumContext";
import { handleError } from "@/utils/error-handlers";

export default {
  name: "UserStoryDetailView",
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
          ...UserStory.getDefaults(),
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
          ...UserStory.getDefaults(),
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
  setup(props, { refs }) {
    // Composables
    const { contextItem } = useScrumContext(props);

    // State
    const item = ref(null);
    const tab = ref("data");
    const showConfirmBeforeLeaving = ref(false);

    // Computed
    const breadcrumbs = computed(() => {
      const currentItemBreadcrumb = {
        text: (item.value && item.value.name) || "Nueva historia de usuario",
        disabled: true,
      };
      if (contextItem.value) {
        let result = [];
        const contextItemBreadcrumb = { text: contextItem.value.name, disabled: false, link: false };
        if (props.sprintId) {
          result = [
            {
              text: "Sprints",
              to: { name: "sprints" },
              exact: true,
            },
            contextItemBreadcrumb,
            {
              text: "Historias de usuario",
              to: { name: "sprint-user-stories", params: { sprintId: props.sprintId } },
              exact: true,
            },
            currentItemBreadcrumb,
          ];
        }
        if (props.epicId) {
          result = [
            {
              text: "Épicas",
              to: { name: "epics" },
              exact: true,
            },
            contextItemBreadcrumb,
            {
              text: "Historias de usuario",
              to: { name: "epic-user-stories", params: { epicId: props.epicId } },
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
    });

    // Watchers
    watch(tab, (newValue, oldValue) => {
      if (oldValue === "data" && showConfirmBeforeLeaving.value) {
        alert("Hay cambios sin guardar en el formulario que podrían perderse al interactuar con otras pestañas.");
      }
    });

    // Methods
    async function fetchItem(id) {
      const response = await UserStoryService.retrieve(id, { expand: "sprint" });
      item.value = response.data;
    }
    function onProgressUpdated() {
      fetchItem(props.id);
      invoke(refs, "progressComponent.fetchItems");
    }
    function onEffortUpdated() {
      fetchItem(props.id);
    }

    return {
      // State
      item,
      tab,
      showConfirmBeforeLeaving,
      // Computed
      contextItem,
      breadcrumbs,
      // Methods
      fetchItem,
      onProgressUpdated,
      onEffortUpdated,
    };
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
