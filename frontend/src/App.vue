<template>
  <v-app id="temat">
    <v-navigation-drawer
      v-model="drawer"
      :class="$vuetify.theme.isDark ? [] : ['grey', 'lighten-3']"
      :expand-on-hover="$vuetify.breakpoint.lgOnly"
      :mini-variant="$vuetify.breakpoint.lgOnly"
      clipped
      app
    >
      <v-list nav dense>
        <template v-for="(item, i) in items">
          <template v-if="!item.staffOnly || (item.staffOnly && loggedUser.is_staff)">
            <v-divider v-if="item.divider" :key="i" dark class="my-3" />

            <v-list-group
              v-else-if="item.items && item.items.length"
              :key="i"
              :prepend-icon="item.icon"
              :color="$vuetify.theme.dark ? 'white' : 'black'"
              no-action
            >
              <template #activator>
                <v-list-item-content>
                  <v-list-item-title>{{ item.text }}</v-list-item-title>
                </v-list-item-content>
              </template>

              <v-list-item v-for="(subitem, j) in item.items" :key="j" link :to="{ name: subitem.route }">
                <v-list-item-content>
                  <v-list-item-title>{{ subitem.text }}</v-list-item-title>
                </v-list-item-content>
                <v-list-item-icon>
                  <v-icon>{{ subitem.icon }}</v-icon>
                </v-list-item-icon>
              </v-list-item>
            </v-list-group>

            <v-list-item v-else :key="i" link :to="{ name: item.route }">
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.text }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </template>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar :color="$vuetify.theme.isDark ? null : 'primary'" dark app fixed clipped-left>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <span class="text-h6 ml-3 mr-5">
        {{ appLabel.name }}
        <sub class="text-caption">{{ appLabel.version }}</sub>
        <img v-if="isXmas" id="santaHat" src="@/assets/santa_hat.svg" alt="Santa's hat" />
      </span>
      <v-spacer />
      <v-progress-circular v-show="loading" class="mr-5" :size="36" color="white" indeterminate />
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

    <v-main :class="$vuetify.theme.isDark ? [] : ['grey', 'lighten-4']">
      <keep-alive>
        <router-view v-if="$route.meta.keepAlive" :key="$route.name" />
      </keep-alive>
      <router-view v-if="!$route.meta.keepAlive" />
    </v-main>

    <v-snackbar v-bind="snackbar" bottom app @input="onSnackbarInput">
      {{ snackbar.message }}
      <template #action="{ attrs }">
        <v-btn icon v-bind="attrs" @click="clearSnackbar">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
import { pick } from "lodash";
import { mapActions, mapGetters, mapMutations, mapState } from "vuex";

import NotificationManager from "@/components/notifications/NotificationManager";

import { isXmas } from "@/utils/dates";
import { handleError } from "@/utils/error-handlers";
import konamiCode from "@/utils/konami-code";
import loperaSentences from "@/utils/lopera-sentences";

export default {
  name: "App",
  metaInfo() {
    return {
      title: "App",
      titleTemplate: `%s | ${this.appLabel.name}`,
    };
  },
  components: { NotificationManager },
  data() {
    return {
      drawer: null,
      items: [
        {
          icon: "mdi-timeline-text",
          text: "Mi timeline",
          route: "timeline",
        },
        { icon: "mdi-calendar-month", text: "Calendario", route: "calendar" },
        {
          icon: "mdi-cards",
          text: "Scrum",
          items: [
            {
              icon: "mdi-sword-cross",
              text: "Épicas",
              route: "epics",
            },
            {
              icon: "mdi-run-fast",
              text: "Sprints",
              route: "sprints",
            },
            {
              icon: "mdi-book-account",
              text: "Historias de usuario",
              route: "user-stories",
            },
            {
              icon: "mdi-weight-lifter",
              text: "Esfuerzo",
              route: "effort",
            },
          ],
        },
        { icon: "mdi-face-agent", text: "Soporte", route: "support" },
        {
          icon: "mdi-briefcase",
          text: "Jornadas especiales",
          route: "green-days",
        },
        {
          icon: "mdi-beach",
          text: "Vacaciones",
          items: [
            {
              icon: "mdi-account",
              text: "Usuario",
              route: "user-holidays",
            },
            {
              icon: "mdi-account-group",
              text: "Equipo",
              route: "team-holidays",
            },
          ],
        },
        { icon: "mdi-baguette", text: "Desayunos", route: "breakfasts" },
        { icon: "mdi-chart-bar", text: "Análisis", route: "analytics" },
        { divider: true, staffOnly: true },
        {
          icon: "mdi-account-key",
          text: "Django Admin",
          route: "admin",
          staffOnly: true,
        },
      ],
      defaultThemeColours: {
        light: pick(this.$vuetify.theme.themes.light, ["primary", "secondary"]),
        dark: pick(this.$vuetify.theme.themes.dark, ["primary", "secondary"]),
      },
    };
  },
  computed: {
    ...mapState(["konamiCodeActive", "loggedUser", "snackbar"]),
    ...mapGetters(["appLabel", "loading"]),
    isXmas,
  },
  watch: {
    "$vuetify.theme.dark": function(newValue) {
      localStorage.darkMode = JSON.stringify(newValue);
    },
    konamiCodeActive(newValue) {
      if (newValue) {
        alert(loperaSentences[Math.floor(Math.random() * loperaSentences.length - 1 + 1)]);
        const betisColours = {
          primary: "#009655",
          secondary: "#d18d2a",
        };
        Object.assign(this.$vuetify.theme.themes.light, betisColours);
        Object.assign(this.$vuetify.theme.themes.dark, betisColours);
      } else {
        Object.assign(this.$vuetify.theme.themes.light, this.defaultThemeColours.light);
        Object.assign(this.$vuetify.theme.themes.dark, this.defaultThemeColours.dark);
      }
    },
  },
  created() {
    this.$vuetify.theme.dark = localStorage.darkMode ? JSON.parse(localStorage.darkMode) : false;
    this.getUsers();
    this.getGroups();
    this.getTags();
  },
  mounted() {
    konamiCode(() => {
      this.toggleKonamiCode();
    });
  },
  errorCaptured(err) {
    handleError(err);
  },
  methods: {
    ...mapActions(["showSnackbar", "clearSnackbar"]),
    ...mapActions("users", ["getUsers", "getGroups"]),
    ...mapActions("tags", ["getTags"]),
    ...mapMutations(["toggleKonamiCode"]),
    onSnackbarInput(value) {
      if (!value) {
        this.clearSnackbar();
      }
    },
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
  position: relative;
  left: -5.3em;
  top: -0.37em;
}
#userMenu {
  cursor: pointer;
}
::v-deep .v-main__wrap {
  padding-bottom: 66px;
}
::v-deep .v-navigation-drawer--mini-variant > .v-navigation-drawer__content {
  overflow: hidden;
}
</style>
