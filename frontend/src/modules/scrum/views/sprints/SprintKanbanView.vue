<template>
  <v-container fluid class="scrolled">
    <ContextBreadcrumbs :items="breadcrumbs" />
    <div id="fs-wrapper" ref="fullscreenWrapper">
      <v-card class="mt-2" :style="{ 'min-width': kanbanMinWidth }">
        <v-toolbar flat>
          <v-toolbar-title class="text-h6">Kanban</v-toolbar-title>
          <v-spacer />
          <SprintViewSelector :sprint-id="sprintId" />
          <v-divider vertical inset class="mx-1" />
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-btn v-if="!hideEmptyColumns" icon v-bind="attrs" @click="hideEmptyColumns = true" v-on="on">
                <v-icon>mdi-eye-off</v-icon>
              </v-btn>
              <v-btn v-else icon v-bind="attrs" @click="hideEmptyColumns = false" v-on="on">
                <v-icon>mdi-eye</v-icon>
              </v-btn>
            </template>
            <span>{{ hideEmptyColumns ? "Mostrar" : "Ocultar" }} columnas vacías</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-btn icon v-bind="attrs" @click="toggleFullscreen" v-on="on">
                <v-icon>{{ isFullscreen ? "mdi-fullscreen-exit" : "mdi-fullscreen" }}</v-icon>
              </v-btn>
            </template>
            <span>{{ isFullscreen ? "Desactivar" : "Activar" }} pantalla completa</span>
          </v-tooltip>
          <v-btn icon :disabled="isLoading" @click="fetchItems">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-toolbar>
        <v-container fluid class="pt-0">
          <v-row class="px-1">
            <template v-for="status in kanbanStatus">
              <v-col v-show="hideEmptyColumns ? itemsByStatus[status.value] : true" :key="status.value" class="px-1">
                <v-card outlined :class="statusColumnClasses">
                  <v-card-title>
                    <v-badge inline v-bind="buildColumnBadgeProps(status)">
                      {{ status.label }}
                    </v-badge>
                  </v-card-title>
                  <v-card-text class="pt-4">
                    <v-skeleton-loader v-if="isLoading" type="card" class="px-1" />
                    <template v-else>
                      <v-row v-for="item in itemsByStatus[status.value]" :key="item.id">
                        <v-col class="px-1">
                          <KanbanCard class="elevation-5 mb-4" :user-story="item" />
                        </v-col>
                      </v-row>
                    </template>
                  </v-card-text>
                </v-card>
              </v-col>
            </template>
          </v-row>
        </v-container>
      </v-card>
    </div>
  </v-container>
</template>

<script>
import { computed, ref } from "@vue/composition-api";
import { useFullscreen } from "@vueuse/core";
import { get, groupBy } from "lodash-es";

import UserStoryService from "@/modules/scrum/services/user-story-service";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import KanbanCard from "@/modules/scrum/components/KanbanCard";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

import { useUserStore } from "@/stores/users";
import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import useLoading from "@/composables/useLoading";
import useScrumContext from "@/modules/scrum/composables/useScrumContext";

export default {
  name: "SprintKanbanView",
  metaInfo() {
    return {
      title: `${get(this.contextItem, "name", "Sprint")} - Kanban`,
    };
  },
  components: { ContextBreadcrumbs, KanbanCard, SprintViewSelector },
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  setup(props, { root }) {
    // Store
    const userStore = useUserStore();
    const userStoryStore = useUserStoryStore();

    // Composables
    const { isLoading, addTask, removeTask } = useLoading();
    const { contextItem } = useScrumContext(props);

    const fullscreenWrapper = ref(null); // will be bound to the fullscreenWrapper <div> element
    const { isFullscreen, toggle: toggleFullscreen } = useFullscreen(fullscreenWrapper);

    // State
    const items = ref([]);
    const hideEmptyColumns = ref(false);

    // Computed
    const kanbanStatus = computed(() => userStoryStore.userStoryStatus.filter((status) => status.value));
    const itemsByStatus = computed(() => {
      return groupBy(items.value, "status");
    });
    const breadcrumbs = computed(() => {
      if (contextItem.value) {
        return [
          {
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          },
          { text: contextItem.value.name, disabled: false, link: false },
          { text: "Kanban", disabled: true },
        ];
      } else {
        return [];
      }
    });
    const kanbanMinWidth = computed(() => {
      const availableColumns = hideEmptyColumns.value ? Object.keys(itemsByStatus.value).length : 4;
      const kanbanWidthByColumns = {
        1: "360px",
        2: "711px",
        3: "1062px",
        4: "1413px",
      };
      return get(kanbanWidthByColumns, [availableColumns]);
    });
    const statusColumnClasses = computed(() => {
      const classes = ["kanban-column", "grey"];
      classes.push(root.$vuetify.theme.isDark ? "darken-3" : "lighten-3");
      return classes;
    });

    // Methods
    async function fetchItems() {
      addTask("fetch-items");
      try {
        const response = await UserStoryService.list({
          sprint_id: props.sprintId,
          status__gte: 1,
          ordering: "status,priority,-risk_level,start_date",
          fields:
            "id,name,status,priority,current_progress,current_progress_changed,validated,validated_changed," +
            "current_effort,planned_effort,start_date,end_date,development_user,validation_user,support_user," +
            "risk_level",
        });
        items.value = response.data;
      } finally {
        removeTask("fetch-items");
      }
    }
    function buildColumnBadgeProps(status) {
      const itemNumber = get(itemsByStatus.value, [status.value, "length"], 0);
      const props = {
        color: "secondary",
        content: `${itemNumber}`,
      };
      if ([2, 3].includes(status.value)) {
        const maxItems = Math.ceil(userStore.workerUsers.length * 1.5);
        props.content = `${itemNumber}/${maxItems}`;
        if (itemNumber > maxItems) {
          props.color = "orange";
        }
      }
      return props;
    }

    // Initialization
    fetchItems();

    return {
      // State
      fullscreenWrapper,
      hideEmptyColumns,
      // Computed
      isLoading,
      contextItem,
      isFullscreen,
      kanbanStatus,
      breadcrumbs,
      itemsByStatus,
      kanbanMinWidth,
      statusColumnClasses,
      // Methods
      toggleFullscreen,
      fetchItems,
      buildColumnBadgeProps,
    };
  },
};
</script>

<style scoped>
.scrolled {
  overflow-x: auto;
}
#fs-wrapper:fullscreen {
  overflow: auto;
}
.kanban-column {
  height: 100%;
}
</style>
