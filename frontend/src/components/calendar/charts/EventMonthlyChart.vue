<template>
  <highcharts :key="theme" :options="chartOptions" />
</template>

<script>
import colors from "vuetify/lib/util/colors";

import ChartMixin from "@/mixins/chart-mixin";

import EventService from "@/services/calendar/event-service";

export default {
  name: "EventMonthlyChart",
  mixins: [ChartMixin({ service: EventService, fetchFunctionName: "monthlyChartData" })],
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
          text: "Eventos por mes"
        },
        xAxis: {
          categories: this.chartData.categories || []
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Cantidad"
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: colors.grey.base
            }
          },
          plotLines: [
            {
              value: this.chartData.average || null,
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
          },
          series: {
            borderWidth: 1,
            borderColor: this.$vuetify.theme.isDark ? "#ffffff" : "rgba(0, 0, 0, 0.54)"
          }
        },
        series: this.chartData.series || []
      };
    }
  }
};
</script>
