<script>
import Highcharts from "highcharts";
import { get } from "lodash";
import colors from "vuetify/lib/util/colors";

import EventService from "@/modules/calendar/services/event-service";

import BaseChart from "@/components/charts/BaseChart";

export default {
  name: "EventAttendeesChart",
  extends: BaseChart,
  data() {
    return {
      service: EventService,
      fetchFunctionName: "attendeesChartData",
    };
  },
  computed: {
    localChartOptions() {
      const series = Highcharts.merge(
        [
          {
            name: "",
            color: colors.green.base,
            data: [],
          },
          {
            name: "",
            color: colors.cyan.base,
            data: [],
          },
        ],
        get(this.chartData, "series", [])
      );
      return {
        chart: {
          type: "packedbubble",
        },
        title: {
          text: "Eventos por invitado",
        },
        tooltip: {
          pointFormat:
            '<tr><td style="color:{series.color};padding:0">Número de invitaciones: </td>' +
            '<td style="padding:0"><strong>{point.y}</strong></td></tr>',
        },
        plotOptions: {
          packedbubble: {
            minSize: "30%",
            maxSize: "120%",
            layoutAlgorithm: {
              splitSeries: false,
              gravitationalConstant: 0.02,
            },
            dataLabels: {
              enabled: true,
              format: "{point.name}",
              style: {
                color: "black",
                fontWeight: "bold",
              },
            },
          },
        },
        series,
      };
    },
  },
};
</script>
