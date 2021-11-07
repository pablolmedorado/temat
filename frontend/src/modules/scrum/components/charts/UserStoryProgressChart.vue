<template>
  <highcharts :key="theme" :constructor-type="'stockChart'" :update-args="[true, true, true]" :options="chartOptions" />
</template>

<script>
import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";
import colors from "vuetify/lib/util/colors";

import darkUnica from "@/utils/highcharts/themes/dark-unica-custom";

export default {
  name: "UserStoryProgressChart",
  components: {
    highcharts: Chart,
  },
  props: {
    chartData: {
      type: Array,
      default: () => [],
    },
    from: {
      type: String,
      default: undefined,
    },
    to: {
      type: String,
      default: undefined,
    },
  },
  computed: {
    plotLines() {
      const result = [];
      if (this.from) {
        result.push({
          value: new Date(this.from).getTime(),
          color: colors.cyan.base,
          dashStyle: "Dash",
          width: 2,
          label: {
            text: "Fecha de inicio plan.",
            style: { color: this.$vuetify.theme.isDark ? "#ffffff" : "#000000" },
          },
        });
      }
      if (this.to) {
        result.push({
          value: new Date(this.to).getTime(),
          color: colors.red.base,
          dashStyle: "Dash",
          width: 2,
          label: {
            text: "Fecha límite",
            style: { color: this.$vuetify.theme.isDark ? "#ffffff" : "#000000" },
          },
        });
      }
      return result;
    },
    localChartOptions() {
      return {
        chart: {
          zoomType: "xy",
          style: {
            fontFamily: "Roboto",
          },
        },
        title: { text: "Historial de avance" },
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
          plotLines: this.plotLines,
          ordinal: false,
        },
        yAxis: {
          allowDecimals: false,
          min: 0,
          max: 100,
          title: {
            text: "% de avance",
          },
        },
        series: [
          {
            name: "Avance",
            type: "spline",
            color: colors.blue.base,
            marker: {
              enabled: true,
              radius: 3,
            },
            data: this.chartData.map((item) => [new Date(item.date).getTime(), item.progress]),
          },
        ],
        navigator: {
          enabled: false,
        },
        credits: { enabled: false },
        exporting: { enabled: true },
        legend: { enabled: true },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><strong>{point.y}%</strong></td></tr>',
          footerFormat: "</table>",
          shared: true,
          useHTML: true,
        },
      };
    },
    theme() {
      return this.$vuetify.theme.isDark ? "dark" : "light";
    },
    chartOptions() {
      const defaultTheme = this.$vuetify.theme.isDark ? darkUnica : Highcharts.getOptions();
      return Highcharts.merge(defaultTheme, this.localChartOptions);
    },
  },
};
</script>
