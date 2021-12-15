<template>
  <v-navigation-drawer
    :value="value"
    :class="$vuetify.theme.isDark ? [] : ['grey', 'lighten-3']"
    :expand-on-hover="$vuetify.breakpoint.lgOnly"
    :mini-variant="$vuetify.breakpoint.lgOnly"
    clipped
    app
    v-on="$listeners"
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
</template>

<script>
import { mapState } from "pinia";

import { useMainStore } from "@/stores/main";

export default {
  name: "AppDrawer",
  props: {
    value: {
      type: Boolean,
      default: undefined,
    },
  },
  data() {
    return {
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
    };
  },
  computed: {
    ...mapState(useMainStore, ["loggedUser"]),
  },
};
</script>

<style scoped>
::v-deep .v-navigation-drawer--mini-variant > .v-navigation-drawer__content {
  overflow: hidden;
}
</style>
