const path = require("path");

const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath: process.env.NODE_ENV === "development" ? "http://localhost:8080/" : "/static/",
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    public: "0.0.0.0:8080",
    https: false,
    headers: { "Access-Control-Allow-Origin": ["*"] },
    hotOnly: true,
    watchOptions: {
      ignored: "./node_modules/",
      aggregateTimeout: 300,
      poll: 1000,
    },
  },
  transpileDependencies: ["vuetify"],
  css: {
    sourceMap: true,
  },
  chainWebpack: (config) => {
    config.plugin("BundleTracker").use(BundleTracker, [
      {
        filename: `./config/webpack-stats-${process.env.NODE_ENV}.json`,
      },
    ]);
    config.resolve.alias.set("__STATIC__", "static");
  },
  configureWebpack: {
    module: {
      rules: [
        {
          test: path.join(__dirname, "src", "utils", "reverse.js"),
          use: [
            {
              loader: "exports-loader",
              options: {
                exports: "default window.Urls",
              },
            },
            {
              loader: "imports-loader",
              options: {
                wrapper: "window",
              },
            },
          ],
        },
      ],
    },
  },
};
