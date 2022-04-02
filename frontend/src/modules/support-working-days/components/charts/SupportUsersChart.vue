<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";
import { get, mean } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import SupportService from "@/modules/support-working-days/services/support-service";

export default {
  name: "SupportUsersChart",
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
      service: SupportService,
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
          text: "Jornadas de soporte por usuario",
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
            name: "Número de jornadas de soporte",
            color: colors.blue.base,
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
