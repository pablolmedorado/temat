module.exports = {
  root: true,
  env: {
    node: true,
    browser: true
  },
  globals: {
    Urls: "readonly"
  },
  extends: ["eslint:recommended", "plugin:vue/recommended", "plugin:prettier/recommended", "prettier/vue"],
  parserOptions: {
    parser: "babel-eslint"
  },
  plugins: ["vue", "prettier", "vuetify"],
  rules: {
    "no-console": process.env.NODE_ENV === "production" ? "warn" : "off",
    "no-debugger": process.env.NODE_ENV === "production" ? "error" : "off",
    "prettier/prettier": "error",
    "vue/component-definition-name-casing": ["error", "PascalCase"],
    "vue/component-name-in-template-casing": ["error", "PascalCase"],
    "vue/component-tags-order": ["error", { order: ["template", "script", "style"] }],
    "vue/match-component-file-name": ["error", { extensions: ["vue"], shouldMatchCase: true }],
    "vue/no-deprecated-scope-attribute": "error",
    "vue/no-deprecated-slot-attribute": "error",
    "vue/no-deprecated-slot-scope-attribute": "error",
    "vue/no-reserved-component-names": "error",
    "vue/no-static-inline-styles": "error",
    "vue/padding-line-between-blocks": "error",
    "vue/require-name-property": "error",
    "vue/valid-v-bind-sync": "error",
    "vuetify/no-deprecated-classes": "error",
    "vuetify/grid-unknown-attributes": "error",
    "vuetify/no-legacy-grid": "error"
  }
};
