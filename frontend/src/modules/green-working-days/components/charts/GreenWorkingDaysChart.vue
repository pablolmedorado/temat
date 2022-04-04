<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";
import { get, mean } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import GreenWorkingDayService from "@/modules/green-working-days/services/green-working-day-service";

export default {
  name: "GreenWorkingDaysChart",
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
      service: GreenWorkingDayService,
      fetchFunctionName: "userChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      return {
        chart: {
          type: "column",
        },
        title: {
          text: "Jornadas especiales por usuario",
        },
        xAxis: {
          categories: get(chartData, "categories", []),
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Jornadas",
          },
          plotLines: [
            {
              value: get(chartData, "data") ? mean(chartData.data) : null,
              color: colors.grey.base,
              dashStyle: "longdash",
              width: 2,
              label: {
                text: "Media",
                style: { color: root.$vuetify.theme.isDark ? "#ffffff" : "#000000" },
              },
            },
          ],
        },
        plotOptions: {
          column: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        legend: { enabled: false },
        series: [
          {
            name: "Número de jornadas especiales",
            color: colors.green.base,
            data: get(chartData, "data", []),
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
