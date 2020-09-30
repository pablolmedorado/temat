<template>
  <highcharts :key="theme" :options="chartOptions" />
</template>

<script>
import { mean } from "lodash";
import colors from "vuetify/lib/util/colors";

import ChartMixin from "@/mixins/chart-mixin";

import SupportService from "@/services/work-organization/support-service";

export default {
  name: "SupportUsersChart",
  mixins: [ChartMixin({ service: SupportService, fetchFunctionName: "userChartData" })],
  data() {
    return {
      chartData: {}
    };
  },
  computed: {
    localChartOptions() {
      return {
        chart: {
          type: "column"
        },
        title: {
          text: "Jornadas de soporte por usuario"
        },
        xAxis: {
          categories: this.chartData.categories || []
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Jornadas"
          },
          plotLines: [
            {
              value: this.chartData.data ? mean(this.chartData.data) : null,
              color: colors.grey.base,
              dashStyle: "longdash",
              width: 2,
              label: {
                text: "Media",
                style: { color: this.$vuetify.theme.isDark ? "#ffffff" : "#000000" }
              }
            }
          ]
        },
        plotOptions: {
          column: {
            dataLabels: {
              enabled: true
            }
          }
        },
        legend: { enabled: false },
        series: [
          {
            name: "Número de jornadas de soporte",
            color: colors.blue.base,
            data: this.chartData.data || []
          }
        ]
      };
    }
  }
};
</script>
