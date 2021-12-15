import Vue from "vue";

import "roboto-fontface/css/roboto/roboto-fontface.css";
import "@mdi/font/css/materialdesignicons.css";

import Vuetify from "vuetify/lib";
import es from "vuetify/es5/locale/es";

Vue.use(Vuetify);

export default new Vuetify({
  lang: {
    locales: { es },
    current: "es",
  },
  theme: {
    dark: localStorage.darkMode ? JSON.parse(localStorage.darkMode) : false,
    themes: {
      light: {
        primary: "#00205b",
        secondary: "#0085ad",
        accent: "#6399ae",
        error: "#e4002b",
        info: "#00aec7",
        success: "#84bd00",
        warning: "#fe5000",
        anchor: "#00205b",
      },
      dark: {
        primary: "#0085ad",
        secondary: "#da1884",
        accent: "#6399ae",
        error: "#e4002b",
        info: "#00aec7",
        success: "#84bd00",
        warning: "#fe5000",
        anchor: "#0085ad",
      },
    },
    options: {
      variations: false,
    },
  },
});
