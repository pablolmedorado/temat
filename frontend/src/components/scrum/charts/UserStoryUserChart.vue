<script>
import { mapState } from "vuex";
import Highcharts from "highcharts";
import { get } from "lodash";

import UserStoryService from "@/services/scrum/user-story-service";

import BaseChart from "@/components/common/BaseChart";

export default {
  name: "UserStoryUserChart",
  extends: BaseChart,
  data() {
    return {
      service: UserStoryService,
      fetchFunctionName: "userChartData",
    };
  },
  computed: {
    ...mapState("scrum", ["effortRoles"]),
    localChartOptions() {
      const series = Highcharts.merge(
        this.effortRoles.map((role) => ({
          name: "",
          color: role.colour,
          data: [],
        })),
        get(this.chartData, "series", [])
      );
      return {
        chart: {
          type: "column",
        },
        title: {
          text: "Historias de usuario por usuario/rol",
        },
        xAxis: {
          categories: get(this.chartData, "categories", []),
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: "Historias de usuario",
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray",
            },
          },
        },
        tooltip: {
          headerFormat: '<span style="font-size:10px">{point.x}</span><table>',
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
            '<td style="padding:0"><strong>{point.y}</strong></td></tr>' +
            '<tr><td style="padding:0">Total: </td>' +
            '<td style="padding:0"><strong>{point.stackTotal}</strong></td></tr>',
          shared: false,
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true,
            },
          },
        },
        series,
      };
    },
  },
};
</script>
