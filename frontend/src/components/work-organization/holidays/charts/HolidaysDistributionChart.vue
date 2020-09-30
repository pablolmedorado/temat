<template>
  <highcharts :key="theme" :constructor-type="'stockChart'" :update-args="[true, true, true]" :options="chartOptions" />
</template>

<script>
import colors from "vuetify/lib/util/colors";

import ChartMixin from "@/mixins/chart-mixin";

import HolidayService from "@/services/work-organization/holiday-service";

export default {
  name: "HolidaysDistributionChart",
  mixins: [ChartMixin({ service: HolidayService, fetchFunctionName: "summary" })],
  computed: {
    localChartOptions() {
      return {
        chart: {
          height: 500,
          zoomType: "xy"
        },
        title: {
          text: "Distribución de solicitudes de vacaciones"
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
              type: "year",
              count: 1,
              text: "1y"
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
            text: "Cantidad"
          }
        },
        series: [
          {
            name: "Solicitudes de vacaciones",
            type: "column",
            color: colors.orange.base,
            data: this.chartData.map(item => [new Date(item.date).getTime(), item.users])
          }
        ]
      };
    }
  }
};
</script>
