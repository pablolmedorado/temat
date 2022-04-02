<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";

import UserStoryService from "@/modules/scrum/services/user-story-service";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

export default {
  name: "EffortRoleChart",
  inheritAttrs: false,
  props: {
    filter: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, { refs, root }) {
    // Store
    const userStoryStore = useUserStoryStore();

    // Computed
    const fetchProps = computed(() => ({
      service: UserStoryService,
      fetchFunctionName: "effortRoleChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      return {
        chart: {
          type: "pie",
        },
        title: {
          text: "Esfuerzo acumulado por rol",
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: { enabled: true, format: "{point.y}UT ({point.percentage:.0f} %)" },
            showInLegend: true,
          },
          series: {
            borderWidth: 1,
            borderColor: root.$vuetify.theme.isDark ? "#ffffff" : "rgba(0, 0, 0, 0.54)",
          },
        },
        series: [
          {
            name: "Unidades de trabajo",
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            data: chartData.map((item) => {
              return {
                ...item,
                name: userStoryStore.effortRolesMap[item.name].label,
                color: userStoryStore.effortRolesMap[item.name].colour,
              };
            }),
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
