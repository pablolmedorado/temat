<script>
import { get, mean } from "lodash";
import colors from "vuetify/lib/util/colors";

import GreenWorkingDayService from "@/modules/green-working-days/services/green-working-day-service";

import BaseChart from "@/components/charts/BaseChart";

export default {
  name: "GreenWorkingDaysChart",
  extends: BaseChart,
  data() {
    return {
      service: GreenWorkingDayService,
      fetchFunctionName: "userChartData",
    };
  },
  computed: {
    localChartOptions() {
      return {
        chart: {
          type: "column",
        },
        title: {
          text: "Jornadas especiales por usuario",
        },
        xAxis: {
          categories: get(this.chartData, "categories", []),
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Jornadas",
          },
          plotLines: [
            {
              value: get(this.chartData, "data") ? mean(this.chartData.data) : null,
              color: colors.grey.base,
              dashStyle: "longdash",
              width: 2,
              label: {
                text: "Media",
                style: { color: this.$vuetify.theme.isDark ? "#ffffff" : "#000000" },
              },
            },
          ],
        },
        plotOptions: {
          column: {
            dataLabels: {
              enabled: true,
            },
          },
        },
        legend: { enabled: false },
        series: [
          {
            name: "Número de jornadas especiales",
            color: colors.green.base,
            data: get(this.chartData, "data", []),
          },
        ],
      };
    },
  },
};
</script>
