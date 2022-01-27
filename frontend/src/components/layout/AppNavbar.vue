<template>
  <v-app-bar :color="$vuetify.theme.isDark ? null : 'primary'" short dark app fixed clipped-left>
    <v-app-bar-nav-icon @click="$emit('toggle:drawer')" />
    <span class="text-h6 ml-3 mr-5">
      {{ appLabel.name }}
      <sub class="text-caption">{{ appLabel.version }}</sub>
      <img v-if="isXmas" id="santaHat" src="@/assets/santa_hat.svg" alt="Santa's hat" />
    </span>
    <v-spacer />
    <v-progress-circular v-show="loadingRequests" class="mr-5" :size="32" color="white" indeterminate />
    <LinkManager />
    <NotificationManager class="mr-5" />
    <UserAvatar size="36" :font-size="14" :user="loggedUser" />
    <v-menu bottom left offset-y>
      <template #activator="{ on, attrs }">
        <v-btn icon v-bind="attrs" v-on="on">
          <v-icon>mdi-dots-vertical</v-icon>
        </v-btn>
      </template>
      <v-list>
        <v-list-item @click="$vuetify.theme.dark = !$vuetify.theme.dark">
          <v-list-item-icon><v-icon>mdi-theme-light-dark</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>Cambiar tema</v-list-item-title></v-list-item-content>
        </v-list-item>
        <v-list-item @click="clearAppData">
          <v-list-item-icon><v-icon>mdi-database-remove-outline</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Restablecer LS y caché</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item :to="{ name: 'logout' }">
          <v-list-item-icon><v-icon>mdi-logout</v-icon></v-list-item-icon>
          <v-list-item-content><v-list-item-title>Logout</v-list-item-title></v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
  </v-app-bar>
</template>

<script>
import { mapActions, mapState } from "pinia";

import LinkManager from "@/modules/links/components/LinkManager";
import NotificationManager from "@/modules/notifications/components/NotificationManager";

import { useMainStore } from "@/stores/main";

import { isXmas } from "@/utils/dates";

export default {
  name: "AppNavbar",
  components: { LinkManager, NotificationManager },
  computed: {
    ...mapState(useMainStore, ["appLabel", "loadingRequests", "loggedUser"]),
    isXmas,
  },
  methods: {
    ...mapActions(useMainStore, ["showSnackbar"]),
    clearAppData() {
      localStorage.clear();
      if (window.caches) {
        caches.keys().then((cacheNames) => {
          cacheNames.forEach((cacheName) => {
            caches.delete(cacheName);
          });
        });
      }
      this.showSnackbar({
        message: "Se ha restablecido el almacenamiento local y la caché",
        timeout: 3000,
      });
    },
  },
};
</script>

<style scoped>
#santaHat {
  height: 20px;
  position: absolute;
  left: 2.73em;
  top: 0.4em;
}
</style>
