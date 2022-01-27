module.exports = {
  presets: ["@vue/cli-plugin-babel/preset", "@babel/preset-env", "@babel/preset-react"],
  plugins: [
    ["@babel/plugin-proposal-class-properties", { loose: true }],
    ["@babel/plugin-proposal-private-property-in-object", { loose: true }],
    ["@babel/plugin-proposal-private-methods", { loose: true }],
  ],
};
