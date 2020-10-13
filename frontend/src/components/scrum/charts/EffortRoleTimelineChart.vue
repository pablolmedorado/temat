<script>
import { mapState } from "vuex";
import { has } from "lodash";

import EffortService from "@/services/scrum/effort-service";

import BaseChart from "@/components/common/BaseChart";

export default {
  name: "EffortRoleTimelineChart",
  extends: BaseChart,
  data() {
    return {
      constructorType: "stockChart",
      service: EffortService,
      fetchFunctionName: "roleTimelineChartData"
    };
  },
  computed: {
    ...mapState("scrum", ["effortRoles"]),
    localChartOptions() {
      return {
        chart: {
          type: "column",
          zoomType: "xy"
        },
        title: {
          text: "Distribución de esfuerzo por rol"
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
            text: "Esfuerzo (UT)"
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray"
            }
          },
          plotBands: [
            {
              from: 0,
              to: 14,
              color: "rgba(68, 170, 213, 0.1)",
              label: {
                text: "Jornada laboral",
                style: {
                  color: this.$vuetify.theme.isDark ? "#ffffff" : "#606060"
                }
              }
            }
          ]
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true
            }
          }
        },
        series: this.effortRoles.map(role => {
          return {
            name: role.label,
            color: role.colour,
            data: has(this.chartData, role.value)
              ? this.chartData[role.value].map(item => [new Date(item.date).getTime(), item.total_effort])
              : []
          };
        })
      };
    }
  }
};
</script>
