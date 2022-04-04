module.exports = {
  preset: "@vue/cli-plugin-unit-jest",
  setupFilesAfterEnv: ["<rootDir>/src/plugins/jest-dom.js"],
  transformIgnorePatterns: ["<rootDir>/node_modules/(?!lodash-es)"],
};
