<template>
  <span class="d-inline-flex">
    <v-menu v-if="menu" bottom left offset-y>
      <template #activator="{ on: onMenu }">
        <v-tooltip bottom>
          <template #activator="{ on: onTooltip }">
            <v-btn icon v-on="{ ...onTooltip, ...onMenu }">
              <v-icon>mdi-view-array</v-icon>
            </v-btn>
          </template>
          <span>Vistas</span>
        </v-tooltip>
      </template>
      <v-list dense>
        <v-list-item
          v-for="view in availableViews"
          :key="view.routeName"
          :to="{ name: view.routeName, params: { sprintId } }"
        >
          <v-list-item-icon>
            <v-icon>{{ view.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-title>{{ view.label }}</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-menu>
    <v-tooltip v-for="view in availableViews" v-else :key="view.routeName" bottom>
      <template #activator="{ on, attrs }">
        <v-btn icon :to="{ name: view.routeName, params: { sprintId } }" v-bind="attrs" v-on="on">
          <v-icon>{{ view.icon }}</v-icon>
        </v-btn>
      </template>
      <span>
        {{ view.label }}
      </span>
    </v-tooltip>
  </span>
</template>

<script>
export default {
  name: "SprintViewSelector",
  props: {
    sprintId: {
      type: String,
      required: true,
    },
    menu: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      views: [
        { label: "Kanban", routeName: "sprint-kanban", icon: "mdi-teach" },
        { label: "Diagrama de quemado (Burn-down/up)", routeName: "sprint-chart", icon: "mdi-fire" },
        { label: "Diagrama de Gantt", routeName: "sprint-gantt", icon: "mdi-chart-timeline" },
        { label: "Informe de despliegue", routeName: "sprint-deployment-report", icon: "mdi-rocket-launch" },
      ],
    };
  },
  computed: {
    availableViews() {
      return this.views.filter((view) => view.routeName !== this.$route.name);
    },
  },
};
</script>
