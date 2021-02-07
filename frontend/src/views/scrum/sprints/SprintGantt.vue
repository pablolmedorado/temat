<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama de Gantt </v-toolbar-title>
        <v-spacer />
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-btn icon :to="{ name: 'sprint-kanban', params: { sprintId } }" v-bind="attrs" v-on="on">
              <v-icon>mdi-teach</v-icon>
            </v-btn>
          </template>
          <span>
            Kanban
          </span>
        </v-tooltip>
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
        <v-divider vertical inset />
        <v-btn icon :disabled="loading" @click="getChartData">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <SprintGanttChart ref="chart" :sprint-id="sprintId" :reactive-filters="false" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

import BreadcrumbsContextMixin from "@/mixins/scrum/breadcrumbs-context-mixin";

import SprintGanttChart from "@/components/scrum/charts/SprintGanttChart";

export default {
  name: "SprintGantt",
  metaInfo: {
    title: "Sprint - Gantt",
  },
  components: { SprintGanttChart },
  mixins: [BreadcrumbsContextMixin],
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  computed: {
    ...mapGetters(["loading"]),
    breadcrumbs() {
      if (this.contextItem) {
        return [
          {
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          },
          { text: this.contextItem.name, disabled: false, link: false },
          { text: "Diagrama de Gantt", disabled: true },
        ];
      } else {
        return [];
      }
    },
  },
  mounted() {
    this.getChartData();
  },
  methods: {
    getChartData() {
      this.$refs.chart.getChartData();
    },
  },
};
</script>
