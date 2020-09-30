<template>
  <highcharts :key="theme" :options="chartOptions" />
</template>

<script>
import ChartMixin from "@/mixins/chart-mixin";

import UserStoryService from "@/services/scrum/user-story-service";

export default {
  name: "UserStoryDelayedChart",
  mixins: [ChartMixin({ service: UserStoryService, fetchFunctionName: "delayedChartData" })],
  computed: {
    localChartOptions() {
      return {
        chart: {
          type: "pie"
        },
        title: {
          text: "Historias de usuario por planificación de fechas"
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: { enabled: true, format: "{point.y} ({point.percentage:.0f} %)" },
            showInLegend: true
          },
          series: {
            borderWidth: 1,
            borderColor: this.$vuetify.theme.isDark ? "#ffffff" : "rgba(0, 0, 0, 0.54)"
          }
        },
        series: [
          {
            name: "Número de historias de usuario",
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            data: this.chartData
          }
        ]
      };
    }
  }
};
</script>
