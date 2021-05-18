/* eslint-disable no-undef */

importScripts("/static/lib/workbox/workbox-sw.js");

if (workbox) {
  var CACHE_PREFIX = "temat";
  var APP_INDEX = "app-index";
  var STATIC_RESOURCES = "static-resources";
  var NOTIFICATIONS = "notifications";
  var LINKS = "links";
  var SELECT_OPTIONS = "select-options";

  workbox.setConfig({
    debug: false,
    modulePathPrefix: "/static/lib/workbox/",
  });

  workbox.core.setCacheNameDetails({ prefix: CACHE_PREFIX });

  self.addEventListener("message", (event) => {
    if (event.data && event.data.type === "SKIP_WAITING") {
      self.skipWaiting();
    }
  });

  workbox.routing.registerRoute(
    function (match) {
      return  ["/", "/accounts/login/"].includes(match.url.pathname);
    },
    new workbox.strategies.NetworkFirst({
      cacheName: APP_INDEX,
    })
  );

  workbox.routing.registerRoute(
    function (match) {
      return (
        match.url.origin === self.location.origin &&
        match.url.pathname.startsWith("/static/")
      );
    },
    new workbox.strategies.StaleWhileRevalidate({
      cacheName: STATIC_RESOURCES,
    })
  );

  workbox.routing.registerRoute(
    new RegExp("/api/common/notifications/unread_count/"),
    new workbox.strategies.NetworkFirst({
      cacheName: NOTIFICATIONS,
    })
  );

  workbox.routing.registerRoute(
    new RegExp("/api/common/links/"),
    new workbox.strategies.StaleWhileRevalidate({
      cacheName: LINKS,
    })
  );

  workbox.routing.registerRoute(
    new RegExp("/api/users/users/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/users/groups/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/calendar/event-types/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/scrum/user-story-types/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/breakfasts/breads/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/breakfasts/bases/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/breakfasts/ingredients/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
  workbox.routing.registerRoute(
    new RegExp("/api/breakfasts/drinks/"),
    new workbox.strategies.NetworkFirst({
      cacheName: SELECT_OPTIONS,
    })
  );
} else {
  console.error("Can't load Workbox!");
}
