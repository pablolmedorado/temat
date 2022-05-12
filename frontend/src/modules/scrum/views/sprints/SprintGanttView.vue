<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama de Gantt </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
        <v-divider vertical inset class="mx-1" />
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
import { computed, onMounted } from "@vue/composition-api";
import { get } from "lodash-es";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import SprintGanttChart from "@/modules/scrum/components/charts/SprintGanttChart";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

import { useLoading } from "@/composables/loading";
import { useScrumContext } from "@/modules/scrum/composables/scrum-context";

export default {
  name: "SprintGanttView",
  metaInfo() {
    return {
      title: `${get(this.contextItem, "name", "Sprint")} - Gantt`,
    };
  },
  components: { ContextBreadcrumbs, SprintGanttChart, SprintViewSelector },
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  setup(props, { refs }) {
    // Composables
    const { isLoading } = useLoading({
      includedChildren: ["chart"],
    });
    const { contextItem } = useScrumContext();

    // Computed
    const breadcrumbs = computed(() => {
      if (contextItem.value) {
        return [
          {
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          },
          { text: contextItem.value.name, disabled: false, link: false },
          { text: "Diagrama de Gantt", disabled: true },
        ];
      } else {
        return [];
      }
    });

    // Methods
    function fetchChartData() {
      refs.chart.fetchData();
    }

    // Lifecycle hooks
    onMounted(fetchChartData);

    return {
      // Computed
      isLoading,
      contextItem,
      breadcrumbs,
      // Methods
      fetchChartData,
    };
  },
};
</script>
