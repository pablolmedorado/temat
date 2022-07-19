import Vue from "vue";

import { render } from "@testing-library/vue";
import VueCompositionApi from "@vue/composition-api";
import Vuetify from "vuetify";

Vue.use(VueCompositionApi);

// We need to use a global Vue instance, otherwise Vuetify will complain about
// read-only attributes.
// This could also be done in a custom Jest-test-setup file to execute for all tests.
// More info: https://github.com/vuetifyjs/vuetify/issues/4068
//            https://vuetifyjs.com/en/getting-started/unit-testing
Vue.use(Vuetify);

// Custom container to integrate Vuetify with Vue Testing Library.
// Vuetify requires you to wrap your app with a v-app component that provides
// a <div data-app="true"> node.
export const renderWithVuetify = (component, options, callback) => {
  const root = document.createElement("div");
  root.setAttribute("data-app", "true");

  return render(
    component,
    {
      container: document.body.appendChild(root),
      // for Vuetify components that use the $vuetify instance property
      vuetify: new Vuetify(),
      ...options,
    },
    callback
  );
};
