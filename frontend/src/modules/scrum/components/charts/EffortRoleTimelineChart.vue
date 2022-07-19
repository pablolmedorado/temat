<template>
  <AsyncChart
    ref="chart"
    constructor-type="stockChart"
    :options-function="buildOptions"
    v-bind="{ ...$attrs, ...fetchProps }"
  />
</template>

<script>
import { computed } from "@vue/composition-api";
import { has } from "lodash-es";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import EffortService from "@/modules/scrum/services/effort-service";

export default {
  name: "EffortRoleTimelineChart",
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
      service: EffortService,
      fetchFunctionName: "roleTimelineChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      return {
        chart: {
          type: "column",
          zoomType: "xy",
        },
        title: {
          text: "Distribución de esfuerzo por rol",
        },
        rangeSelector: {
          buttons: [
            {
              type: "week",
              count: 1,
              text: "1w",
            },
            {
              type: "month",
              count: 1,
              text: "1m",
            },
            {
              type: "all",
              count: 1,
              text: "All",
            },
          ],
        },
        xAxis: {
          ordinal: false,
        },
        yAxis: {
          allowDecimals: false,
          min: 0,
          title: {
            text: "Esfuerzo (UT)",
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray",
            },
          },
          plotBands: [
            {
              from: 0,
              to: 14,
              color: "rgba(68, 170, 213, 0.1)",
              label: {
                text: "Jornada laboral",
                style: {
                  color: root.$vuetify.theme.isDark ? "#ffffff" : "#606060",
                },
              },
            },
          ],
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true,
            },
          },
        },
        series: userStoryStore.effortRoles.map((role) => {
          return {
            name: role.label,
            color: role.colour,
            data: has(chartData, role.value)
              ? chartData[role.value].map((item) => [new Date(item.date).getTime(), item.total_effort])
              : [],
          };
        }),
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
