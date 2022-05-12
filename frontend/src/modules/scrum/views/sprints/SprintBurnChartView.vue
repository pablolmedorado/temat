<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama {{ burnUp ? "Burn-Up" : "Burn-Down" }} </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
        <v-divider vertical inset class="mx-1" />
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-btn v-if="!burnUp" icon :disabled="isLoading" v-bind="attrs" @click="burnUp = true" v-on="on">
              <v-icon>mdi-trending-up</v-icon>
            </v-btn>
            <v-btn v-else icon :disabled="isLoading" v-bind="attrs" @click="burnUp = false" v-on="on">
              <v-icon>mdi-trending-down</v-icon>
            </v-btn>
          </template>
          <span>Cambiar sentido ({{ burnUp ? "Burn-Down" : "Burn-Up" }})</span>
        </v-tooltip>
        <v-btn icon :disabled="isLoading" @click="fetchChartData">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      <v-card-text>
        <SprintBurnChart ref="chart" :sprint-id="sprintId" :burn-up="burnUp" :reactive-filters="false" />
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import { computed, onMounted, ref } from "@vue/composition-api";
import { get } from "lodash-es";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import SprintBurnChart from "@/modules/scrum/components/charts/SprintBurnChart";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

import { useLoading } from "@/composables/loading";
import { useScrumContext } from "@/modules/scrum/composables/scrum-context";

export default {
  name: "SprintBurnChartView",
  metaInfo() {
    return {
      title: `${get(this.contextItem, "name", "Sprint")} - Gráfica`,
    };
  },
  components: { ContextBreadcrumbs, SprintBurnChart, SprintViewSelector },
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

    // State
    const burnUp = ref(false);

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
          { text: "Diagrama de quemado", disabled: true },
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
      // State
      burnUp,
      // Computed
      isLoading,
      breadcrumbs,
      // Methods
      fetchChartData,
    };
  },
};
</script>
