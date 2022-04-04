<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";
import { get } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import EventService from "@/modules/calendar/services/event-service";

export default {
  name: "EventMonthlyChart",
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
      service: EventService,
      fetchFunctionName: "monthlyChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      return {
        chart: {
          type: "column",
        },
        title: {
          text: "Eventos por mes",
        },
        xAxis: {
          categories: get(chartData, "categories", []),
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Cantidad",
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: colors.grey.base,
            },
          },
          plotLines: [
            {
              value: get(chartData, "average", null),
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
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.x}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><strong>{point.y}</strong></td></tr>' +
            '<tr><td style="padding:0">Total: </td>' +
            '<td style="padding:0"><strong>{point.stackTotal}</strong></td></tr>',
          shared: false,
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true,
            },
          },
          series: {
            borderWidth: 1,
            borderColor: root.$vuetify.theme.isDark ? "#ffffff" : "rgba(0, 0, 0, 0.54)",
          },
        },
        series: get(chartData, "series", []),
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
