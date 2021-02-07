<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama de Gantt </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
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
import SprintViewSelector from "@/components/scrum/SprintViewSelector";

export default {
  name: "SprintGantt",
  metaInfo: {
    title: "Sprint - Gantt",
  },
  components: { SprintGanttChart, SprintViewSelector },
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
