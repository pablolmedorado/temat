<template>
  <v-container fluid class="scrolled">
    <ContextBreadcrumbs :items="breadcrumbs" />
    <div id="fs-wrapper" ref="fullscreenWrapper">
      <v-card class="mt-2" :style="{ 'min-width': kanbanMinWidth }">
        <v-toolbar flat>
          <v-toolbar-title class="text-h6">Kanban</v-toolbar-title>
          <v-spacer />
          <SprintViewSelector :sprint-id="sprintId" />
          <v-divider vertical inset />
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
                          <KanbanCard class="mb-4" :user-story="item" />
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
import { ref } from "@vue/composition-api";
import { mapGetters, mapState } from "vuex";
import { useFullscreen } from "@vueuse/core";
import { get, groupBy } from "lodash";

import UserStoryService from "@/modules/scrum/services/user-story-service";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import KanbanCard from "@/modules/scrum/components/KanbanCard";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

import useLoading from "@/composables/useLoading";
import useScrumContext from "@/modules/scrum/composables/useScrumContext";

export default {
  name: "SprintKanbanView",
  metaInfo: {
    title: "Sprint - Kanban",
  },
  components: { ContextBreadcrumbs, KanbanCard, SprintViewSelector },
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { isLoading, addTask, removeTask } = useLoading();

    const { contextItem } = useScrumContext(props);

    const fullscreenWrapper = ref(null); // will be bind to the fullscreenWrapper <div> element
    const { isFullscreen, toggle: toggleFullscreen } = useFullscreen(fullscreenWrapper);

    return {
      isLoading,
      addTask,
      removeTask,
      contextItem,
      fullscreenWrapper,
      isFullscreen,
      toggleFullscreen,
    };
  },
  data() {
    return {
      items: [],
      hideEmptyColumns: false,
    };
  },
  computed: {
    ...mapState("scrum", ["userStoryStatus"]),
    ...mapGetters("users", ["workerUsers"]),
    kanbanStatus() {
      return this.userStoryStatus.filter((status) => status.value);
    },
    itemsByStatus() {
      return groupBy(this.items, "status");
    },
    breadcrumbs() {
      if (this.contextItem) {
        return [
          {
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          },
          { text: this.contextItem.name, disabled: false, link: false },
          { text: "Kanban", disabled: true },
        ];
      } else {
        return [];
      }
    },
    kanbanMinWidth() {
      if (this.hideEmptyColumns) {
        const availableStatus = Object.keys(this.itemsByStatus).length;
        switch (availableStatus) {
          case 1:
            return "360px";
          case 2:
            return "711px";
          case 3:
            return "1062px";
          case 4:
            return "1413px";
          default:
            return undefined;
        }
      } else {
        return "1413px";
      }
    },
    statusColumnClasses() {
      return this.$vuetify.theme.isDark ? ["grey", "darken-3"] : ["grey", "lighten-3"];
    },
  },
  created() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      this.addTask("fetch-items");
      try {
        const response = await UserStoryService.list({
          sprint_id: this.sprintId,
          status__gte: 1,
          ordering: "status,priority,-risk_level,start_date",
          fields:
            "id,name,status,priority,current_progress,current_progress_changed,validated,validated_changed," +
            "actual_effort,planned_effort,start_date,end_date,development_user,validation_user,support_user," +
            "risk_level",
        });
        this.items = response.data;
      } finally {
        this.removeTask("fetch-items");
      }
    },
    buildColumnBadgeProps(status) {
      const itemNumber = get(this.itemsByStatus, [status.value, "length"], 0);
      const props = {
        color: "secondary",
        content: `${itemNumber}`,
      };
      if ([2, 3].includes(status.value)) {
        const maxItems = Math.ceil(this.workerUsers.length * 1.5);
        props.content = `${itemNumber}/${maxItems}`;
        if (itemNumber > maxItems) {
          props.color = "orange";
        }
      }
      return props;
    },
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
</style>
