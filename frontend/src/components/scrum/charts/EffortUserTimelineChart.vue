<script>
import { mapGetters } from "vuex";
import { has } from "lodash";

import EffortService from "@/services/scrum/effort-service";

import BaseChart from "@/components/common/BaseChart";

export default {
  name: "EffortUserTimelineChart",
  extends: BaseChart,
  data() {
    return {
      service: EffortService,
      fetchFunctionName: "userTimelineChartData",
    };
  },
  computed: {
    ...mapGetters("users", ["workerUsers"]),
    localChartOptions() {
      return {
        chart: {
          type: "column",
          zoomType: "xy",
        },
        title: {
          text: "Distribución de esfuerzo por usuario",
        },
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
          ordinal: false,
        },
        yAxis: {
          allowDecimals: false,
          min: 0,
          title: {
            text: "Esfuerzo (UT)",
          },
          stackLabels: {
            enabled: true,
            style: {
              fontWeight: "bold",
              color: "gray",
            },
          },
          plotBands: [
            {
              from: 0,
              to: this.workerUsers.length * 14,
              color: "rgba(68, 170, 213, 0.1)",
              label: {
                text: "Jornada laboral",
                style: {
                  color: this.$vuetify.theme.isDark ? "#ffffff" : "#606060",
                },
              },
            },
          ],
        },
        plotOptions: {
          column: {
            stacking: "normal",
            dataLabels: {
              enabled: true,
            },
          },
        },
        series: this.workerUsers.map((user) => {
          return {
            name: user.acronym,
            data: has(this.chartData, user.acronym)
              ? this.chartData[user.acronym].map((item) => [new Date(item.date).getTime(), item.total_effort])
              : [],
          };
        }),
      };
    },
  },
};
</script>
