<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";

import UserStoryService from "@/modules/scrum/services/user-story-service";

export default {
  name: "UserStoryTypeChart",
  inheritAttrs: false,
  props: {
    filter: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, { refs, root }) {
    // Computed
    const fetchProps = computed(() => ({
      service: UserStoryService,
      fetchFunctionName: "typeChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      return {
        chart: {
          type: "pie",
        },
        title: {
          text: "Historias de usuario por tipo",
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: { enabled: true, format: "{point.y} ({point.percentage:.0f} %)" },
            showInLegend: true,
          },
          series: {
            borderWidth: 1,
            borderColor: root.$vuetify.theme.isDark ? "#ffffff" : "rgba(0, 0, 0, 0.54)",
          },
        },
        series: [
          {
            name: "Número de historias de usuario",
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            data: chartData || [],
          },
        ],
      };
    }
    function fetchData() {
      refs.chart.fetchData();
    }

    return {
      // Computed
      fetchProps,
      // Methods
      buildOptions,
      fetchData,
    };
  },
};
</script>
