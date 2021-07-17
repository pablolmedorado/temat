<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama de Gantt </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
        <v-divider vertical inset />
        <v-btn icon :disabled="isLoading" @click="fetchChartData">
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
import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import SprintGanttChart from "@/modules/scrum/components/charts/SprintGanttChart";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

import useLoading from "@/composables/useLoading";
import useScrumContext from "@/modules/scrum/composables/useScrumContext";

export default {
  name: "SprintGantt",
  metaInfo: {
    title: "Sprint - Gantt",
  },
  components: { ContextBreadcrumbs, SprintGanttChart, SprintViewSelector },
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { isLoading } = useLoading({
      includedChildren: ["chart"],
    });
    const { contextItem } = useScrumContext(props);
    return {
      isLoading,
      contextItem,
    };
  },
  computed: {
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
    this.fetchChartData();
  },
  methods: {
    fetchChartData() {
      this.$refs.chart.fetchChartData();
    },
  },
};
</script>
