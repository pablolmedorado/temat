// Imports
import Vue from "vue";
import Vuetify from "vuetify";
import { makeDecorator } from "@storybook/addons";

// Utilities
import deepmerge from "deepmerge";

// Vuetify
import "vuetify/dist/vuetify.min.css";
import "@mdi/font/css/materialdesignicons.min.css";

Vue.use(Vuetify);

export default makeDecorator({
  name: "withVuetify",
  parameterName: "vuetify",
  wrapper: (storyFn, context, { parameters = {} }) => {
    // Reduce to one new URL?
    const searchParams = new URL(window.location).searchParams;
    const dark = searchParams.get("eyes-variation") === "dark";
    const rtl = searchParams.get("eyes-variation") === "rtl";
    const vuetify = new Vuetify(
      deepmerge(
        {
          rtl,
          theme: {
            dark,
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
          },
        },
        parameters
      )
    );
    const WrappedComponent = storyFn(context);

    // eslint-disable-next-line vue/require-name-property
    return Vue.extend({
      vuetify,
      components: { WrappedComponent },
      template: `
        <v-app>
          <v-container fluid>
            <wrapped-component />
          </v-container>
        </v-app>
      `,
    });
  },
});
