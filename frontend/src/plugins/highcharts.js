import Vue from "vue";

import Highcharts from "highcharts";
import moreInit from "highcharts/highcharts-more";
import stockInit from "highcharts/modules/stock";
import exportingInit from "highcharts/modules/exporting";
import HighchartsVue from "highcharts-vue";

moreInit(Highcharts);
stockInit(Highcharts);
exportingInit(Highcharts);

Vue.use(HighchartsVue);
