<template>
  <highcharts :key="theme" :options="chartOptions" />
</template>

<script>
import Highcharts from "highcharts";
import colors from "vuetify/lib/util/colors";

import ChartMixin from "@/mixins/chart-mixin";

import GreenService from "@/services/work-organization/green-service";

export default {
  name: "GreenWorkingDaysChart",
  mixins: [ChartMixin({ service: GreenService, fetchFunctionName: "userChartData" })],
  data() {
    return {
      chartData: {}
    };
  },
  computed: {
    localChartOptions() {
      const series = Highcharts.merge(
        [
          { name: "", color: colors.green.base, data: [] },
          { name: "", color: colors.lime.base, data: [] }
        ],
        this.chartData.series || []
      );
      return {
        chart: {
          type: "column"
        },
        title: {
          text: "Jornadas especiales por usuario"
        },
        xAxis: {
          categories: this.chartData.categories || []
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Jornadas"
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray"
            }
          }
        },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.x}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><strong>{point.y}</strong></td></tr>' +
            '<tr><td style="padding:0">Total: </td>' +
            '<td style="padding:0"><strong>{point.stackTotal}</strong></td></tr>',
          shared: false
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true
            }
          }
        },
        series
      };
    }
  }
};
</script>
