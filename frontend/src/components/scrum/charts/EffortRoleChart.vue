<script>
import { mapGetters } from "vuex";

import UserStoryService from "@/services/scrum/user-story-service";

import BaseChart from "@/components/common/BaseChart";

export default {
  name: "EffortRoleChart",
  extends: BaseChart,
  data() {
    return {
      service: UserStoryService,
      fetchFunctionName: "effortRoleChartData",
    };
  },
  computed: {
    ...mapGetters("scrum", ["effortRolesMap"]),
    localChartOptions() {
      return {
        chart: {
          type: "pie",
        },
        title: {
          text: "Esfuerzo acumulado por rol",
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: "pointer",
            dataLabels: { enabled: true, format: "{point.y}UT ({point.percentage:.0f} %)" },
            showInLegend: true,
          },
          series: {
            borderWidth: 1,
            borderColor: this.$vuetify.theme.isDark ? "#ffffff" : "rgba(0, 0, 0, 0.54)",
          },
        },
        series: [
          {
            name: "Unidades de trabajo",
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            data: this.chartData.map((item) => {
              return {
                ...item,
                name: this.effortRolesMap[item.name].label,
                color: this.effortRolesMap[item.name].colour,
              };
            }),
          },
        ],
      };
    },
  },
};
</script>
