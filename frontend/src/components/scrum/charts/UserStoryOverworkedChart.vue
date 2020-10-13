<script>
import UserStoryService from "@/services/scrum/user-story-service";

import BaseChart from "@/components/common/BaseChart";

export default {
  name: "UserStoryOverworkedChart",
  extends: BaseChart,
  data() {
    return {
      service: UserStoryService,
      fetchFunctionName: "overworkedChartData"
    };
  },
  computed: {
    localChartOptions() {
      return {
        chart: {
          type: "pie"
        },
        title: {
          text: "Historias de usuario por planificación de esfuerzo"
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
            data: this.chartData || []
          }
        ]
      };
    }
  }
};
</script>
