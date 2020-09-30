import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";

import darkUnica from "@/utils/highcharts/themes/dark-unica-custom";

export default function ChartMixin({ service, fetchFunctionName }) {
  if (!service || !fetchFunctionName) {
    throw new Error("service and fetchFunctionName params are mandatory");
  }

  return {
    components: {
      highcharts: Chart
    },
    props: {
      filter: {
        type: Object,
        default: () => ({})
      },
      reactiveFilters: {
        type: Boolean,
        required: false,
        default: true
      }
    },
    data() {
      return {
        service,
        fetchFunctionName,
        chartData: [],
        defaultChartOptions: {
          title: { text: "Análisis" },
          chart: {
            style: {
              fontFamily: "Roboto"
            }
          },
          credits: { enabled: false },
          exporting: { enabled: true },
          legend: { enabled: true },
          tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat:
              '<tr><td style="color:{series.color};padding:0">{series.name}: </td>' +
              '<td style="padding:0"><strong>{point.y:.1f}</strong></td></tr>',
            footerFormat: "</table>",
            shared: true,
            useHTML: true
          },
          series: []
        }
      };
    },
    computed: {
      theme() {
        return this.$vuetify.theme.isDark ? "dark" : "light";
      },
      localChartOptions() {
        throw new Error("localChartOptions not implemented");
      },
      chartOptions() {
        const defaultTheme = this.$vuetify.theme.isDark ? darkUnica : Highcharts.getOptions();
        return Highcharts.merge(defaultTheme, this.defaultChartOptions, this.localChartOptions);
      }
    },
    watch: {
      filter: {
        deep: true,
        immediate: true,
        handler() {
          if (this.reactiveFilters) {
            this.getChartData();
          }
        }
      }
    },
    activated() {
      this.getChartData();
    },
    methods: {
      buildFetchFunctionArgs() {
        return [this.filter];
      },
      async getChartData() {
        const response = await this.service[this.fetchFunctionName].apply(this.service, this.buildFetchFunctionArgs());
        this.chartData = response.data;
      }
    }
  };
}
