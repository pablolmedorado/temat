<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama {{ burnUp ? "Burn-Up" : "Burn-Down" }} </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
        <v-divider vertical inset />
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
import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import SprintBurnChart from "@/modules/scrum/components/charts/SprintBurnChart";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";

import useLoading from "@/composables/useLoading";
import useScrumContext from "@/modules/scrum/composables/useScrumContext";

export default {
  name: "SprintBurnChartView",
  metaInfo: {
    title: "Sprint - Gráfica",
  },
  components: { ContextBreadcrumbs, SprintBurnChart, SprintViewSelector },
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
  data() {
    return {
      burnUp: false,
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
          { text: "Diagrama de quemado", disabled: true },
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
