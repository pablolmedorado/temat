<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Diagrama {{ burnUp ? "Burn-Up" : "Burn-Down" }} </v-toolbar-title>
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
            <v-btn v-if="!burnUp" icon :disabled="loading" v-bind="attrs" @click="burnUp = true" v-on="on">
              <v-icon>mdi-trending-up</v-icon>
            </v-btn>
            <v-btn v-else icon :disabled="loading" v-bind="attrs" @click="burnUp = false" v-on="on">
              <v-icon>mdi-trending-down</v-icon>
            </v-btn>
          </template>
          <span>Cambiar sentido ({{ burnUp ? "Burn-Down" : "Burn-Up" }})</span>
        </v-tooltip>
        <v-btn icon :disabled="loading" @click="getChartData">
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
import { mapGetters } from "vuex";

import BreadcrumbsContextMixin from "@/mixins/scrum/breadcrumbs-context-mixin";

import SprintBurnChart from "@/components/scrum/charts/SprintBurnChart";

export default {
  name: "SprintChart",
  metaInfo: {
    title: "Sprint - Gráfica",
  },
  components: { SprintBurnChart },
  mixins: [BreadcrumbsContextMixin],
  data() {
    return {
      burnUp: false,
    };
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
          { text: "Diagrama de quemado", disabled: true },
        ];
      } else {
        return [];
      }
    },
  },
  methods: {
    getChartData() {
      this.$refs.chart.getChartData();
    },
  },
};
</script>
