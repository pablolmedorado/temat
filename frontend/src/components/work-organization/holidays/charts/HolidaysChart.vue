<script>
import Highcharts from "highcharts";
import { get } from "lodash";
import colors from "vuetify/lib/util/colors";

import HolidayService from "@/services/work-organization/holiday-service";

import BaseChart from "@/components/common/BaseChart";

import { hex2rgba } from "@/utils/colours";

export default {
  name: "HolidaysChart",
  extends: BaseChart,
  data() {
    return {
      service: HolidayService,
      fetchFunctionName: "userAvailabilityChartData"
    };
  },
  computed: {
    localChartOptions() {
      const series = Highcharts.merge(
        [
          {
            name: "",
            color: hex2rgba(colors.amber.base, "1"),
            data: [],
            pointPadding: 0.3
          },
          {
            name: "",
            color: hex2rgba(colors.deepOrange.base, ".9"),
            data: [],
            pointPadding: 0.4
          }
        ],
        get(this.chartData, "series", [])
      );
      return {
        chart: {
          type: "column"
        },
        title: {
          text: "Vacaciones por usuario"
        },
        xAxis: {
          categories: get(this.chartData, "categories", [])
        },
        yAxis: [
          {
            min: 0,
            title: {
              text: "Días"
            }
          }
        ],
        plotOptions: {
          column: {
            grouping: false,
            shadow: false,
            borderWidth: 0
          }
        },
        series
      };
    }
  }
};
</script>
