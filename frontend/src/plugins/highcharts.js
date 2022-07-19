import Vue from "vue";

import Highcharts from "highcharts";
import HighchartsVue from "highcharts-vue";
import moreInit from "highcharts/highcharts-more";
import exportingInit from "highcharts/modules/exporting";
import ganttInit from "highcharts/modules/gantt";
import stockInit from "highcharts/modules/stock";

moreInit(Highcharts);
stockInit(Highcharts);
ganttInit(Highcharts);
exportingInit(Highcharts);

Vue.use(HighchartsVue);
