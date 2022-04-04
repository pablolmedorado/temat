<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";
import Highcharts from "highcharts";
import { get } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import HolidayService from "@/modules/holidays/services/holiday-service";

import { hex2rgba } from "@/utils/colours";

export default {
  name: "HolidaysChart",
  inheritAttrs: false,
  props: {
    filter: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, { refs }) {
    // Computed
    const fetchProps = computed(() => ({
      service: HolidayService,
      fetchFunctionName: "userAvailabilityChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      const series = Highcharts.merge(
        [
          {
            name: "",
            color: hex2rgba(colors.amber.base, "1"),
            data: [],
            pointPadding: 0.3,
          },
          {
            name: "",
            color: hex2rgba(colors.deepOrange.base, ".9"),
            data: [],
            pointPadding: 0.4,
          },
        ],
        get(chartData, "series", [])
      );
      return {
        chart: {
          type: "column",
        },
        title: {
          text: "Vacaciones por usuario",
        },
        xAxis: {
          categories: get(chartData, "categories", []),
        },
        yAxis: [
          {
            min: 0,
            title: {
              text: "Días",
            },
          },
        ],
        plotOptions: {
          column: {
            grouping: false,
            shadow: false,
            borderWidth: 0,
          },
        },
        series,
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
