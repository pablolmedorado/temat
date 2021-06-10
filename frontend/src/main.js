import Vue from "vue";

import "./plugins/composition";

import router from "./router";
import store from "./store/index";

import "roboto-fontface/css/roboto/roboto-fontface.css";
import "@mdi/font/css/materialdesignicons.css";
import vuetify from "./plugins/vuetify";

import "./plugins/highcharts";

import "./plugins/reverse";

import "./plugins/global-components";

import App from "./App.vue";

Vue.config.productionTip = false;

// eslint-disable-next-line vue/require-name-property
export default new Vue({
  el: "#app",
  router,
  store,
  vuetify,
  render: (h) => h(App),
});
