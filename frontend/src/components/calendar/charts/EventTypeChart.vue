<template>
  <highcharts :key="theme" :options="chartOptions" />
</template>

<script>
import ChartMixin from "@/mixins/chart-mixin";

import EventService from "@/services/calendar/event-service";

export default {
  name: "EventTypeChart",
  mixins: [ChartMixin({ service: EventService, fetchFunctionName: "typeChartData" })],
  computed: {
    localChartOptions() {
      return {
        chart: {
          type: "pie"
        },
        title: {
          text: "Eventos por tipo"
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
            name: "Número de eventos",
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
