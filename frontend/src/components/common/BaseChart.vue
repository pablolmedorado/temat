<template>
  <div>
    <highcharts
      v-if="chartData"
      :key="theme"
      :constructor-type="constructorType"
      :update-args="[true, true, true]"
      :options="chartOptions"
    />
    <v-card v-else :height="height || 400" flat>
      <v-overlay absolute>
        <v-progress-circular indeterminate size="64"></v-progress-circular>
      </v-overlay>
    </v-card>
  </div>
</template>

<script>
import Highcharts from "highcharts";
import { Chart } from "highcharts-vue";

import darkUnica from "@/utils/highcharts/themes/dark-unica-custom";

export default {
  name: "BaseChart",
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
      default: true
    },
    height: {
      type: Number,
      default: 400
    }
  },
  data() {
    return {
      service: null,
      fetchFunctionName: null,
      chartData: null,
      constructorType: "chart",
      defaultChartOptions: {
        title: { text: "Análisis" },
        chart: {
          height: this.height,
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
    // eslint-disable-next-line vue/return-in-computed-property
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
      handler() {
        if (this.reactiveFilters) {
          this.getChartData();
        }
      },
      deep: true,
      immediate: true
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
</script>
