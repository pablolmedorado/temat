// Imports
import "~storybook/addon-composition-api";
import { configure, addDecorator } from "@storybook/vue";
import { withA11y } from "@storybook/addon-a11y";
import { withKnobs } from "@storybook/addon-knobs";
import { withTemplate } from "~storybook/addon-show-vue-markup";
import { withVuetify } from "~storybook/addon-vuetify";
import StoryRouter from "storybook-vue-router";

addDecorator(withA11y);
addDecorator(withKnobs);
addDecorator(withTemplate);
addDecorator(withVuetify);
addDecorator(StoryRouter());

configure(require.context("./stories", true, /\.stories\.js$/), module);
