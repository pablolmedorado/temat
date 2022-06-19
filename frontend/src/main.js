/* eslint-disable import/order */
import Vue from "vue";

import "./plugins/composition";

import pinia from "./plugins/pinia";
import vuetify from "./plugins/vuetify";
import router from "./router";

import "./plugins/highcharts";

import "./plugins/global-components";

import App from "./App.vue";

Vue.config.productionTip = false;

// eslint-disable-next-line vue/require-name-property
export default new Vue({
  el: "#app",
  router,
  pinia,
  vuetify,
  render: (h) => h(App),
});
