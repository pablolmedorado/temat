// Imports
import { addDecorator } from "@storybook/vue";
import StoryRouter from "storybook-vue-router";

import { withVuetify } from "~storybook/addon-vuetify";
import { withTemplate } from "~storybook/addon-show-vue-markup";

import "@/plugins/composition";
import "@/plugins/global-components";

addDecorator(StoryRouter());
addDecorator(withVuetify);
addDecorator(withTemplate);
