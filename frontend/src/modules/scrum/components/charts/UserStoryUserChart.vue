<template>
  <AsyncChart ref="chart" :options-function="buildOptions" v-bind="{ ...$attrs, ...fetchProps }" />
</template>

<script>
import { computed } from "@vue/composition-api";
import Highcharts from "highcharts";
import { get } from "lodash-es";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import UserStoryService from "@/modules/scrum/services/user-story-service";

export default {
  name: "UserStoryUserChart",
  inheritAttrs: false,
  props: {
    filter: {
      type: Object,
      default: () => ({}),
    },
  },
  setup(props, { refs }) {
    // Store
    const userStoryStore = useUserStoryStore();

    // Computed
    const fetchProps = computed(() => ({
      service: UserStoryService,
      fetchFunctionName: "userChartData",
      fetchFunctionArgs: [props.filter],
    }));

    // Methods
    function buildOptions(chartData) {
      const series = Highcharts.merge(
        userStoryStore.effortRoles.map((role) => ({
          name: "",
          color: role.colour,
          data: [],
        })),
        get(chartData, "series", [])
      );
      return {
        chart: {
          type: "column",
        },
        title: {
          text: "Historias de usuario por usuario/rol",
        },
        xAxis: {
          categories: get(chartData, "categories", []),
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Historias de usuario",
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray",
            },
          },
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
