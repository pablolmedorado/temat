module.exports = {
  root: true,
  env: {
    node: true,
    browser: true
  },
  globals: {
    Urls: "readonly"
  },
  extends: ["plugin:vue/recommended", "eslint:recommended", "@vue/prettier"],
  parserOptions: {
    parser: "babel-eslint"
  },
  plugins: ["vuetify"],
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
    "prettier/prettier": "error",
    "vue/component-definition-name-casing": ["error", "PascalCase"],
    "vue/component-name-in-template-casing": ["error", "PascalCase"],
    "vue/component-tags-order": ["error", { order: ["template", "script", "style"] }],
    "vue/custom-event-name-casing": "off", // TODO: activate after migrating to vue3/vuetify3
    "vue/match-component-file-name": ["error", { extensions: ["vue"], shouldMatchCase: true }],
    "vue/no-deprecated-scope-attribute": "error",
    "vue/no-deprecated-slot-attribute": "error",
    "vue/no-deprecated-slot-scope-attribute": "error",
    "vue/no-reserved-component-names": "error",
    "vue/no-static-inline-styles": "error",
    "vue/padding-line-between-blocks": "error",
    "vue/require-name-property": "error",
    "vue/valid-v-bind-sync": "error",
    "vue/valid-v-slot": "off", // TODO: activate after migrating to vue3/vuetify3
    "vuetify/no-deprecated-classes": "error",
    "vuetify/grid-unknown-attributes": "error",
    "vuetify/no-legacy-grid": "error"
  }
};
