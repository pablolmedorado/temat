<template>
  <highcharts :key="theme" :options="chartOptions" />
</template>

<script>
import Highcharts from "highcharts";
import colors from "vuetify/lib/util/colors";

import ChartMixin from "@/mixins/chart-mixin";

import HolidayService from "@/services/work-organization/holiday-service";

import { hex2rgba } from "@/utils/colours";

export default {
  name: "HolidaysChart",
  mixins: [ChartMixin({ service: HolidayService, fetchFunctionName: "userAvailabilityChartData" })],
  data() {
    return {
      chartData: {}
    };
  },
  computed: {
    localChartOptions() {
      const series = Highcharts.merge(
        [
          {
            name: "",
            color: hex2rgba(colors.amber.base, "1"),
            data: [],
            pointPadding: 0.3
          },
          {
            name: "",
            color: hex2rgba(colors.deepOrange.base, ".9"),
            data: [],
            pointPadding: 0.4
          }
        ],
        this.chartData.series || []
      );
      return {
        chart: {
          type: "column"
        },
        title: {
          text: "Vacaciones por usuario"
        },
        xAxis: {
          categories: this.chartData.categories || []
        },
        yAxis: [
          {
            min: 0,
            title: {
              text: "Días"
            }
          }
        ],
        plotOptions: {
          column: {
            grouping: false,
            shadow: false,
            borderWidth: 0
          }
        },
        series
      };
    }
  }
};
</script>
