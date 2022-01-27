// Imports
import Vue from "vue";
import { makeDecorator } from "@storybook/addons";

import pinia from "@/plugins/pinia";

export default makeDecorator({
  name: "withPinia",
  parameterName: "pinia",
  wrapper: (storyFn, context) => {
    const story = storyFn(context);

    // eslint-disable-next-line vue/require-name-property
    return Vue.extend({
      pinia,
      components: { story },
      template: `
        <story />
      `,
    });
  },
});
