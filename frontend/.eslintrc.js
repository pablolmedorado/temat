const path = require("path");

module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
  },
  extends: [
    "plugin:vue/recommended",
    "plugin:testing-library/vue",
    "plugin:storybook/recommended",
    "eslint:recommended",
    "plugin:import/recommended",
    "@vue/prettier",
  ],
  parserOptions: {
    parser: "babel-eslint",
  },
  plugins: ["vuetify"],
  rules: {
    "import/order": [
      "error",
      {
        groups: ["builtin", "external", "internal", ["parent", "sibling"]],
        pathGroups: [
          {
            pattern: "vue+(|-router|x)",
            group: "external",
            position: "before",
          },
          {
            pattern: "**/models/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/stores/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/services/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/mixins/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/views/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/components/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/composables/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/utils/**",
            group: "internal",
            position: "before",
          },
          {
            pattern: "**/assets/**",
            group: "internal",
            position: "after",
          },
        ],
        pathGroupsExcludedImportTypes: ["vue+(|x|tify)"],
        "newlines-between": "always",
        alphabetize: {
          order: "asc",
          caseInsensitive: true,
        },
      },
    ],
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
    "prettier/prettier": "error",
    "testing-library/prefer-screen-queries": "off",
    "vue/component-definition-name-casing": ["error", "PascalCase"],
    "vue/component-name-in-template-casing": ["error", "PascalCase"],
    "vue/component-tags-order": [
      "error",
      {
        order: ["template", "script", "style"],
      },
    ],
    "vue/custom-event-name-casing": "off", // TODO: activate after migrating to vue3/vuetify3
    "vue/match-component-file-name": [
      "error",
      {
        extensions: ["vue"],
        shouldMatchCase: true,
      },
    ],
    "vue/max-attributes-per-line": "off",
    "vue/no-deprecated-scope-attribute": "error",
    "vue/no-deprecated-slot-attribute": "error",
    "vue/no-deprecated-slot-scope-attribute": "error",
    "vue/no-reserved-component-names": "error",
    "vue/no-static-inline-styles": "error",
    "vue/padding-line-between-blocks": "error",
    "vue/require-name-property": "error",
    "vue/valid-v-bind-sync": "error",
    "vue/valid-v-slot": "off", // TODO: activate after migrating to vue3/vuetify3
    "vuetify/grid-unknown-attributes": "error",
    "vuetify/no-deprecated-classes": "error",
    "vuetify/no-deprecated-components": "error",
    "vuetify/no-legacy-grid": "error",
  },
  overrides: [
    {
      files: ["**/__tests__/*.{j,t}s?(x)", "**/tests/unit/**/*.spec.{j,t}s?(x)"],
      env: {
        jest: true,
      },
    },
  ],
  settings: {
    "import/resolver": {
      webpack: {
        config: {
          resolve: {
            alias: {
              "@": path.resolve("src"),
            },
            extensions: [".js", ".vue"],
          },
        },
      },
    },
  },
};
