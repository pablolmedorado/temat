<template>
  <v-app-bar :color="$vuetify.theme.isDark ? null : 'primary'" short dark app fixed clipped-left>
    <v-app-bar-nav-icon @click="$emit('toggle:drawer')" />
    <span class="text-h6 ml-3 mr-5">
      {{ appLabel.name }}
      <sub class="text-caption">{{ appLabel.version }}</sub>
      <img v-if="isXmas" id="santaHat" src="@/assets/santa_hat.svg" alt="Santa's hat" />
    </span>
    <v-spacer />
    <v-progress-circular v-show="loading" class="mr-5" :size="36" color="white" indeterminate />
    <LinkManager />
    <NotificationManager class="mr-5" />
    <v-menu bottom left offset-y>
      <template #activator="{ on, attrs }">
        <span id="userMenu" v-bind="attrs" v-on="on">
          <span class="mr-3">{{ loggedUser.first_name }}</span>
          <UserAvatar size="36" :font-size="14" :user="loggedUser" />
          <v-icon right>mdi-menu-down</v-icon>
        </span>
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
import { mapActions, mapGetters, mapState } from "vuex";

import LinkManager from "@/components/links/LinkManager";
import NotificationManager from "@/components/notifications/NotificationManager";

import { isXmas } from "@/utils/dates";

export default {
  name: "AppNavbar",
  components: { LinkManager, NotificationManager },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["appLabel", "loading"]),
    isXmas,
  },
  methods: {
    ...mapActions(["showSnackbar"]),
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
#userMenu {
  cursor: pointer;
}
</style>
