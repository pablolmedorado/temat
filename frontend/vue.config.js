const BundleTracker = require("webpack-bundle-tracker");

module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/static/" : "http://localhost:8080/",
  transpileDependencies: ["vuetify"],
  devServer: {
    host: "0.0.0.0",
    port: 8080,
    https: false,
    headers: { "Access-Control-Allow-Origin": ["*"] },
    hotOnly: true,
    watchOptions: {
      ignored: "./node_modules/",
      aggregateTimeout: 300,
      poll: 1000
    }
  },
  chainWebpack: config => {
    config.plugin("BundleTracker").use(BundleTracker, [
      {
        filename: `./config/webpack-stats-${process.env.NODE_ENV}.json`
      }
    ]);
    config.resolve.alias.set("__STATIC__", "static");
  }
};
