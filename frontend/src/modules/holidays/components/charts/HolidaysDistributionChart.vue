<script>
import colors from "vuetify/lib/util/colors";

import HolidayService from "@/modules/holidays/services/holiday-service";

import BaseChart from "@/components/charts/BaseChart";

export default {
  name: "HolidaysDistributionChart",
  extends: BaseChart,
  data() {
    return {
      constructorType: "stockChart",
      service: HolidayService,
      fetchFunctionName: "summary",
    };
  },
  computed: {
    localChartOptions() {
      const data = this.chartData || [];
      return {
        chart: {
          zoomType: "xy",
        },
        title: {
          text: "Distribución de solicitudes de vacaciones",
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
              type: "year",
              count: 1,
              text: "1y",
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
            text: "Cantidad",
          },
        },
        series: [
          {
            name: "Solicitudes de vacaciones",
            type: "column",
            color: colors.orange.base,
            data: data.map((item) => [new Date(item.date).getTime(), item.users]),
          },
        ],
      };
    },
  },
};
</script>
