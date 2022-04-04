<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";
import Highcharts from "highcharts";
import { get } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import EventService from "@/modules/calendar/services/event-service";

export default {
  name: "EventAttendeesChart",
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
      service: EventService,
      fetchFunctionName: "attendeesChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      const series = Highcharts.merge(
        [
          {
            name: "",
            color: colors.green.base,
            data: [],
          },
          {
            name: "",
            color: colors.cyan.base,
            data: [],
          },
        ],
        get(chartData, "series", [])
      );
      return {
        chart: {
          type: "packedbubble",
        },
        title: {
          text: "Eventos por invitado",
        },
        tooltip: {
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">Número de invitaciones: </td>' +
            '<td style="padding:0"><strong>{point.y}</strong></td></tr>',
        },
        plotOptions: {
          packedbubble: {
            minSize: "30%",
            maxSize: "120%",
            layoutAlgorithm: {
              splitSeries: false,
              gravitationalConstant: 0.02,
            },
            dataLabels: {
              enabled: true,
              format: "{point.name}",
              style: {
                color: "black",
                fontWeight: "bold",
              },
            },
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
