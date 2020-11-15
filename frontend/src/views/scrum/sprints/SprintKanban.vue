<template>
  <v-container fluid class="scrolled">
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card id="kanban-card" class="mt-2" :style="{ 'min-width': kanbanMinWidth }">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">Kanban</v-toolbar-title>
        <v-spacer />
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-btn icon :to="{ name: 'sprint-chart', params: { sprintId } }" v-bind="attrs" v-on="on">
              <v-icon>mdi-fire</v-icon>
            </v-btn>
          </template>
          <span>
            Diagrama de quemado (Burn-down/up)
          </span>
        </v-tooltip>
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-btn icon :to="{ name: 'sprint-gantt', params: { sprintId } }" v-bind="attrs" v-on="on">
              <v-icon>mdi-chart-timeline</v-icon>
            </v-btn>
          </template>
          <span>
            Diagrama de Gantt
          </span>
        </v-tooltip>
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
            <v-btn v-if="!fullscreenEnabled" icon v-bind="attrs" @click="activateFullscreen" v-on="on">
              <v-icon>mdi-fullscreen</v-icon>
            </v-btn>
            <v-btn v-else icon v-bind="attrs" @click="deactivateFullscreen" v-on="on">
              <v-icon>mdi-fullscreen-exit</v-icon>
            </v-btn>
          </template>
          <span>{{ fullscreenEnabled ? "Desactivar" : "Activar" }} pantalla completa</span>
        </v-tooltip>
        <v-btn icon :disabled="loading" @click="fetchItems">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      <v-container fluid class="pt-0">
        <v-row class="px-1">
          <template v-for="status in kanbanStatus">
            <v-col v-show="hideEmptyColumns ? itemsByStatus[status.value] : true" :key="status.value" class="px-1">
              <v-card outlined :class="statusColumnClasses">
                <v-card-title>{{ status.label }}</v-card-title>
                <v-card-text>
                  <v-skeleton-loader v-if="loading" type="card" class="px-1" />
                  <template v-else>
                    <v-row v-for="item in itemsByStatus[status.value]" :key="item.id">
                      <v-col class="px-1">
                        <KanbanCard :user-story="item" />
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
  </v-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { groupBy } from "lodash";

import BreadcrumbsContextMixin from "@/mixins/scrum/breadcrumbs-context-mixin";

import UserStoryService from "@/services/scrum/user-story-service";

import KanbanCard from "@/components/scrum/KanbanCard";

export default {
  name: "SprintKanban",
  metaInfo: {
    title: "Sprint - Kanban",
  },
  components: { KanbanCard },
  mixins: [BreadcrumbsContextMixin],
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      items: [],
      hideEmptyColumns: false,
      fullscreenEnabled: false,
    };
  },
  computed: {
    ...mapGetters(["loading"]),
    ...mapState("scrum", ["userStoryStatus"]),
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
            return "355px";
          case 2:
            return "655px";
          case 3:
            return "955px";
          case 4:
            return "1255px";
          default:
            return undefined;
        }
      } else {
        return "1255px";
      }
    },
    statusColumnClasses() {
      return this.$vuetify.theme.isDark ? ["grey", "darken-3"] : ["grey", "lighten-3"];
    },
  },
  activated() {
    this.fetchItems();
    document.addEventListener("fullscreenchange", this.onFullscreenChange);
  },
  deactivated() {
    document.removeEventListener("fullscreenchange", this.onFullscreenChange);
  },
  methods: {
    async fetchItems() {
      const response = await UserStoryService.list({
        sprint_id: this.sprintId,
        status__gte: 1,
        ordering: "status,priority,-risk_level",
        fields:
          "id,name,status,priority,current_progress,current_progress_changed,validated,validated_changed,actual_effort,planned_effort,end_date,development_user,validation_user,support_user,risk_level",
      });
      this.items = response.data;
    },
    activateFullscreen() {
      const element = document.getElementById("kanban-card");
      if (element.requestFullscreen) {
        element.requestFullscreen(); // W3C spec
      } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen(); // Firefox
      } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullscreen(); // Safari
      }
    },
    deactivateFullscreen() {
      if (document.exitFullscreen) {
        document.exitFullscreen(); // W3C spec
      } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen(); // Firefox
      } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen(); // Safari
      }
    },
    onFullscreenChange() {
      const fullscreenElement =
        document.fullscreenElement || // W3C spec
        document.mozFullScreenElement || // Firefox
        document.webkitFullscreenElement; // Safari
      this.fullscreenEnabled = Boolean(fullscreenElement);
    },
  },
};
</script>

<style lang="scss" scoped>
.scrolled {
  overflow-x: auto;
}
</style>
