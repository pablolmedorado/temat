<template>
  <highcharts :key="theme" :constructor-type="'stockChart'" :update-args="[true, true, true]" :options="chartOptions" />
</template>

<script>
import { mapGetters } from "vuex";
import colors from "vuetify/lib/util/colors";

import ChartMixin from "@/mixins/chart-mixin";

import SprintService from "@/services/scrum/sprint-service";

export default {
  name: "SprintBurnChart",
  mixins: [ChartMixin({ service: SprintService, fetchFunctionName: "burnChartData" })],
  props: {
    sprintId: {
      type: String,
      required: true
    },
    burnUp: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      chartData: {}
    };
  },
  computed: {
    ...mapGetters("users", ["usersWithCompany"]),
    totalEffort() {
      return this.chartData.total_effort || 0;
    },
    dailyProgress() {
      return this.chartData.data ? this.totalEffort / this.chartData.data.length : 0;
    },
    actualData() {
      if (this.chartData.data) {
        return this.chartData.data.map(item => {
          const timestamp = new Date(item.date).getTime();
          let value = null;
          if (item.effort_burned !== null) {
            if (this.burnUp) {
              value = item.effort_burned;
            } else {
              value = this.totalEffort - item.effort_burned;
            }
          }
          return [timestamp, value];
        });
      }
      return [];
    },
    idealData() {
      if (this.chartData.data) {
        return this.chartData.data.map((item, index) => {
          const timestamp = new Date(item.date).getTime();
          let value;
          if (this.burnUp) {
            value = (index + 1) * this.dailyProgress;
          } else {
            value = this.totalEffort - (index + 1) * this.dailyProgress;
          }
          return [timestamp, value];
        });
      }
      return [];
    },
    effortData() {
      if (this.chartData.data) {
        return this.chartData.data.map(item => [new Date(item.date).getTime(), item.actual_effort]);
      }
      return [];
    },
    localChartOptions() {
      return {
        chart: {
          height: 500,
          zoomType: "xy"
        },
        title: { text: null },
        rangeSelector: {
          buttons: [
            {
              type: "week",
              count: 1,
              text: "1w"
            },
            {
              type: "month",
              count: 1,
              text: "1m"
            },
            {
              type: "all",
              count: 1,
              text: "All"
            }
          ]
        },
        xAxis: {
          ordinal: false
        },
        yAxis: {
          allowDecimals: false,
          min: 0,
          title: {
            text: "Esfuerzo (UT)"
          },
          plotLines: [
            {
              value: this.usersWithCompany.length * 14,
              color: colors.grey.base,
              dashStyle: "Dash",
              width: 1,
              zIndex: 4,
              label: {
                align: "right",
                x: -20,
                text: "Esfuerzo diario esperado"
              }
            }
          ]
        },
        series: [
          {
            name: `${this.burnUp ? "Acumulado" : "Remanente"} real`,
            type: "line",
            color: colors.blue.base,
            zIndex: 3,
            marker: {
              enabled: true,
              radius: 3
            },
            data: this.actualData
          },
          {
            name: `${this.burnUp ? "Acumulado" : "Remanente"} ideal`,
            type: "line",
            dashStyle: "longdash",
            color: colors.lightGreen.base,
            zIndex: 2,
            data: this.idealData
          },
          {
            name: "Esfuerzo real",
            type: "column",
            color: colors.teal.lighten4,
            zIndex: 1,
            data: this.effortData
          }
        ],
        navigator: {
          enabled: false
        }
      };
    }
  },
  methods: {
    buildFetchFunctionArgs() {
      return [this.sprintId];
    }
  }
};
</script>
