<script>
import { get, mean } from "lodash";
import colors from "vuetify/lib/util/colors";

import SupportService from "@/services/work-organization/support-service";

import BaseChart from "@/components/common/BaseChart";

export default {
  name: "SupportUsersChart",
  extends: BaseChart,
  data() {
    return {
      service: SupportService,
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
          text: "Jornadas de soporte por usuario",
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
            name: "Número de jornadas de soporte",
            color: colors.blue.base,
            data: get(this.chartData, "data", []),
          },
        ],
      };
    },
  },
};
</script>
