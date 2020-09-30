<template>
  <highcharts :key="theme" :constructor-type="'stockChart'" :update-args="[true, true, true]" :options="chartOptions" />
</template>

<script>
import { mapState } from "vuex";

import ChartMixin from "@/mixins/chart-mixin";

import EffortService from "@/services/scrum/effort-service";

export default {
  name: "EffortRoleTimelineChart",
  mixins: [ChartMixin({ service: EffortService, fetchFunctionName: "roleTimelineChartData" })],
  data() {
    return {
      chartData: {}
    };
  },
  computed: {
    ...mapState("scrum", ["effortRoles"]),
    localChartOptions() {
      return {
        chart: {
          type: "column",
          height: 500,
          zoomType: "xy"
        },
        title: {
          text: "Distribución de esfuerzo por rol"
        },
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
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray"
            }
          },
          plotBands: [
            {
              from: 0,
              to: 14,
              color: "rgba(68, 170, 213, 0.1)",
              label: {
                text: "Jornada laboral",
                style: {
                  color: this.$vuetify.theme.isDark ? "#ffffff" : "#606060"
                }
              }
            }
          ]
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true
            }
          }
        },
        series: this.effortRoles.map(role => {
          return {
            name: role.label,
            color: role.colour,
            data: this.chartData[role.value]
              ? this.chartData[role.value].map(item => [new Date(item.date).getTime(), item.total_effort])
              : []
          };
        })
      };
    }
  }
};
</script>
