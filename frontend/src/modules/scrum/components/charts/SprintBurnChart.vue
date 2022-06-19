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
import { has, get } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import { useUserStore } from "@/stores/users";

import SprintService from "@/modules/scrum/services/sprint-service";

export default {
  name: "SprintBurnChart",
  inheritAttrs: false,
  props: {
    sprintId: {
      type: String,
      required: true,
    },
    burnUp: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { refs }) {
    // Store
    const userStore = useUserStore();

    // Computed
    const fetchProps = computed(() => ({
      service: SprintService,
      fetchFunctionName: "burnChartData",
      fetchFunctionArgs: [props.sprintId],
    }));

    // Methods
    function buildOptions(chartData) {
      const totalEffort = get(chartData, "total_effort", 0);
      const dailyProgress = has(chartData, "data") ? totalEffort / chartData.data.length : 0;

      let actualData, idealData, effortData;
      if (has(chartData, "data")) {
        actualData = chartData.data.map((item) => {
          const timestamp = new Date(item.date).getTime();
          let value = null;
          if (item.effort_burned !== null) {
            if (props.burnUp) {
              value = item.effort_burned;
            } else {
              value = totalEffort - item.effort_burned;
            }
          }
          return [timestamp, value];
        });
        idealData = chartData.data.map((item, index) => {
          const timestamp = new Date(item.date).getTime();
          let value;
          if (props.burnUp) {
            value = (index + 1) * dailyProgress;
          } else {
            value = totalEffort - (index + 1) * dailyProgress;
          }
          return [timestamp, value];
        });
        effortData = chartData.data.map((item) => [new Date(item.date).getTime(), item.current_effort]);
      } else {
        actualData = [];
        idealData = [];
        effortData = [];
      }

      return {
        chart: {
          zoomType: "xy",
        },
        title: { text: null },
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
          plotLines: [
            {
              value: userStore.workerUsers.length * 14,
              color: colors.grey.base,
              dashStyle: "Dash",
              width: 1,
              zIndex: 4,
              label: {
                align: "right",
                x: -20,
                text: "Esfuerzo diario esperado",
              },
            },
          ],
        },
        series: [
          {
            name: `${props.burnUp ? "Acumulado" : "Remanente"} real`,
            type: "line",
            color: colors.blue.base,
            zIndex: 3,
            marker: {
              enabled: true,
              radius: 3,
            },
            data: actualData,
          },
          {
            name: `${props.burnUp ? "Acumulado" : "Remanente"} ideal`,
            type: "line",
            dashStyle: "longdash",
            color: colors.lightGreen.base,
            zIndex: 2,
            data: idealData,
          },
          {
            name: "Esfuerzo real",
            type: "column",
            color: colors.teal.lighten4,
            zIndex: 1,
            data: effortData,
          },
        ],
        navigator: {
          enabled: false,
        },
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
