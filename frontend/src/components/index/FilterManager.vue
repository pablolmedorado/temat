<template>
  <div>
    <v-menu bottom left offset-y>
      <template #activator="{ on: menu }">
        <v-tooltip bottom>
          <template #activator="{ on: tooltip }">
            <v-btn icon :disabled="disabled" v-on="{ ...tooltip, ...menu }">
              <v-badge :value="advancedFiltersCount" color="primary" dot overlap>
                <v-icon>mdi-filter-menu</v-icon>
              </v-badge>
            </v-btn>
          </template>
          <span>Filtros</span>
        </v-tooltip>
      </template>
      <v-list dense>
        <v-list-item v-if="advancedFilters" @click.stop="$emit('open:config-dialog')">
          <v-list-item-icon>
            <v-badge :value="advancedFiltersCount" color="primary" :content="advancedFiltersCount" overlap>
              <v-icon>mdi-filter</v-icon>
            </v-badge>
          </v-list-item-icon>
          <v-list-item-title>Filtros avanzados</v-list-item-title>
        </v-list-item>
        <v-list-item @click="$emit('clear:filters')">
          <v-list-item-icon>
            <v-icon>mdi-eraser</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Limpiar</v-list-item-title>
        </v-list-item>
        <v-list-item @click.stop="$refs.quickFilterDialog.open()">
          <v-list-item-icon>
            <v-icon>mdi-filter-plus-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-title>Guardar filtro rápido</v-list-item-title>
        </v-list-item>
        <v-divider class="mt-3 mb-2" />
        <v-subheader class="ml-2">Filtros rápidos</v-subheader>
        <v-list-item
          v-for="filter in quickFilters"
          :key="filter.label"
          :class="isEqual(filter.filters, filters) ? 'v-list-item--active' : ''"
          @click="$emit('apply:filter', filter)"
        >
          <v-list-item-title>{{ filter.label }}</v-list-item-title>
          <v-list-item-action class="my-0">
            <v-btn icon @click.stop="pinQuickFilter(filter)">
              <v-icon v-if="pinnedQuickFilter === filter.key" color="primary">mdi-pin</v-icon>
              <v-icon v-else>mdi-pin-outline</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
        <v-list-item
          v-for="filter in customQuickFilters"
          :key="filter.label"
          :class="isEqual(filter.filters, filters) ? 'v-list-item--active' : ''"
          @click="$emit('apply:filter', filter)"
        >
          <v-list-item-title>{{ filter.label }}</v-list-item-title>
          <v-list-item-action class="my-0">
            <v-btn icon @click.stop="deleteQuickFilter(filter)">
              <v-icon color="error">mdi-delete</v-icon>
            </v-btn>
          </v-list-item-action>
        </v-list-item>
      </v-list>
    </v-menu>

    <QuickFilterDialog ref="quickFilterDialog" :quick-filters="customQuickFilters" @add:quick-filter="addQuickFilter" />
  </div>
</template>

<script>
import { mapActions } from "pinia";
import { isEqual, isObject } from "lodash";

import { useMainStore } from "@/stores/main";

import useLocalStorage from "@/composables/useLocalStorage";

export default {
  name: "FilterManager",
  props: {
    localStorageNamespace: {
      type: String,
      required: true,
    },
    filters: {
      type: Object,
      default: () => ({}),
    },
    advancedFilters: {
      type: Boolean,
      default: false,
    },
    advancedFiltersCount: {
      type: Number,
      required: true,
    },
    quickFilters: {
      type: Array,
      default: () => [],
    },
    pinnedQuickFilter: {
      type: String,
      default: undefined,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const customQuickFilters = useLocalStorage(`${props.localStorageNamespace}QuickFilters`, []);
    return {
      customQuickFilters,
    };
  },
  methods: {
    isEqual,
    ...mapActions(useMainStore, ["showSnackbar"]),
    addQuickFilter(filter) {
      if (isObject(filter)) {
        filter.filters = { ...this.filters };
      } else {
        this.customQuickFilters.push({
          label: filter,
          filters: { ...this.filters },
        });
      }
      this.showSnackbar({
        color: "success",
        message: "Filtro guardado correctamente",
      });
    },
    pinQuickFilter(filter) {
      this.$emit("update:pinned-quick-filter", filter.key);
      this.showSnackbar({ message: `Se ha fijado el filtro "${filter.label}"` });
    },
    deleteQuickFilter(filter) {
      this.customQuickFilters = this.customQuickFilters.filter((item) => item.label !== filter.label);
      this.showSnackbar({
        color: "success",
        message: "Filtro eliminado correctamente",
      });
    },
  },
};
</script>
