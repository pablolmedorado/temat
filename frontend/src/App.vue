<template>
  <v-app id="temat">
    <AppDrawer v-model="drawer" />
    <AppNavbar @toggle:drawer="drawer = !drawer" />

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
import { mapActions, mapGetters, mapState } from "vuex";
import { useMutations } from "vuex-composition-helpers";
import { pick } from "lodash";

import AppDrawer from "@/components/layout/AppDrawer";
import AppNavbar from "@/components/layout/AppNavbar";

import useKonamiCode from "@/composables/useKonamiCode";
import loperaSentences from "@/utils/lopera-sentences";
import { handleError } from "@/utils/error-handlers";

export default {
  name: "App",
  metaInfo() {
    return {
      title: "App",
      titleTemplate: `%s | ${this.appLabel.name}`,
    };
  },
  components: { AppDrawer, AppNavbar },
  setup() {
    const { toggleKonamiCode } = useMutations(["toggleKonamiCode"]);
    useKonamiCode(() => toggleKonamiCode());
  },
  data() {
    return {
      drawer: null,
      defaultThemeColours: {
        light: pick(this.$vuetify.theme.themes.light, ["primary", "secondary"]),
        dark: pick(this.$vuetify.theme.themes.dark, ["primary", "secondary"]),
        betis: { primary: "#009655", secondary: "#d18d2a" },
      },
    };
  },
  computed: {
    ...mapState(["konamiCodeActive", "snackbar"]),
    ...mapGetters(["appLabel"]),
  },
  watch: {
    "$vuetify.theme.dark": function (newValue) {
      localStorage.darkMode = JSON.stringify(newValue);
    },
    konamiCodeActive(newValue) {
      this.onKonamiCodeChange(newValue);
    },
  },
  created() {
    this.getUsers();
    this.getGroups();
    this.getTags();
  },
  errorCaptured(err) {
    handleError(err);
  },
  methods: {
    ...mapActions(["clearSnackbar"]),
    ...mapActions("users", ["getUsers", "getGroups"]),
    ...mapActions("tags", ["getTags"]),
    onSnackbarInput(value) {
      if (!value) {
        this.clearSnackbar();
      }
    },
    onKonamiCodeChange(value) {
      if (value) {
        alert(loperaSentences[Math.floor(Math.random() * loperaSentences.length - 1 + 1)]);
      }
      const themeColours = {
        light: this.defaultThemeColours[value ? "betis" : "light"],
        dark: this.defaultThemeColours[value ? "betis" : "dark"],
      };
      Object.assign(this.$vuetify.theme.themes.light, themeColours.light);
      Object.assign(this.$vuetify.theme.themes.dark, themeColours.dark);
    },
  },
};
</script>

<style scoped>
::v-deep .v-main__wrap {
  padding-bottom: 66px;
}
</style>
