<template>
  <v-app id="temat">
    <AppDrawer v-model="drawer" />
    <AppNavbar @toggle:drawer="drawer = !drawer" />

    <v-main :class="$vuetify.theme.isDark ? [] : ['grey', 'lighten-4']">
      <keep-alive :max="25">
        <router-view v-if="$route.meta.keepAlive" :key="$route.path" />
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
import { onErrorCaptured, ref, toRefs, watch } from "@vue/composition-api";
import { pick } from "lodash-es";

import { useMainStore } from "@/stores/main";
import { useTagStore } from "@/stores/tags";
import { useUserStore } from "@/stores/users";

import { useKonamiCode } from "@/composables/konami-code";

import { handleError } from "@/utils/error-handlers";
import loperaSentences from "@/utils/lopera-sentences";

export default {
  name: "App",
  metaInfo() {
    return {
      title: "App",
      titleTemplate: `%s | ${this.appLabel.name}`,
    };
  },
  setup(props, { root }) {
    // Store
    const mainStore = useMainStore();
    const tagStore = useTagStore();
    const userStore = useUserStore();

    // State
    const drawer = ref(null);

    // Computed
    const { appLabel, snackbar } = toRefs(mainStore);

    // Theme
    const themes = root.$vuetify.theme.themes;
    const defaultThemeColours = {
      light: pick(themes.light, ["primary", "secondary"]),
      dark: pick(themes.dark, ["primary", "secondary"]),
      betis: { primary: "#009655", secondary: "#d18d2a" },
    };
    watch(
      () => root.$vuetify.theme.isDark,
      (newValue) => localStorage.setItem("darkMode", JSON.stringify(newValue))
    );

    // Snackbar
    function onSnackbarInput(value) {
      if (!value) {
        mainStore.clearSnackbar();
      }
    }

    // Konami Code
    function onKonamiCodeChange(value) {
      const themeColours = {
        light: defaultThemeColours[value ? "betis" : "light"],
        dark: defaultThemeColours[value ? "betis" : "dark"],
      };
      Object.assign(root.$vuetify.theme.themes.light, themeColours.light);
      Object.assign(root.$vuetify.theme.themes.dark, themeColours.dark);
      if (value) {
        alert(loperaSentences[Math.floor(Math.random() * loperaSentences.length - 1 + 1)]);
      }
    }
    watch(() => mainStore.isKonamiCodeActive, onKonamiCodeChange);

    // Lifecycle hooks
    onErrorCaptured((error) => {
      handleError(error);
    });

    // Initialization
    userStore.getUsers();
    userStore.getGroups();
    tagStore.getTags();
    useKonamiCode(() => mainStore.toggleKonamiCode());

    return {
      // State
      drawer,
      // Computed
      appLabel,
      // Snackbar
      snackbar,
      clearSnackbar: mainStore.clearSnackbar,
      onSnackbarInput,
    };
  },
};
</script>

<style scoped>
::v-deep .v-main__wrap {
  padding-bottom: 66px;
}
</style>
