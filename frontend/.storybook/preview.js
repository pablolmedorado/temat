// Imports
import { addDecorator } from "@storybook/vue";
import StoryRouter from "storybook-vue-router";

import { withPinia } from "~storybook/addon-pinia";
import { withVuetify } from "~storybook/addon-vuetify";
import { withTemplate } from "~storybook/addon-show-vue-markup";

import "@/plugins/composition";
import "@/plugins/global-components";

import { routes } from "@/router";

addDecorator(StoryRouter({}, { routes }));
addDecorator(withPinia);
addDecorator(withVuetify);
addDecorator(withTemplate);
