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
import colors from "vuetify/lib/util/colors";

import HolidayService from "@/modules/holidays/services/holiday-service";

export default {
  name: "HolidaysDistributionChart",
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
      fetchFunctionName: "summary",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      const data = chartData || [];
      return {
        chart: {
          zoomType: "xy",
        },
        title: {
          text: "Distribución de solicitudes de vacaciones",
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
              type: "year",
              count: 1,
              text: "1y",
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
            text: "Cantidad",
          },
        },
        series: [
          {
            name: "Solicitudes de vacaciones",
            type: "column",
            color: colors.orange.base,
            data: data.map((item) => [new Date(item.date).getTime(), item.users]),
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
