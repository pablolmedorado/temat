module.exports = {
  stories: ["./stories/**/*.stories.js"],
  addons: [
    "@storybook/addon-docs",
    "@storybook/addon-controls",
    "./addon-show-vue-markup/register",
    "@storybook/addon-actions",
    "@storybook/addon-viewport",
  ],
};
