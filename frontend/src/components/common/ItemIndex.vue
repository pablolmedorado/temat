<template>
  <div>
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          <slot name="title" v-bind="{ verboseName, verboseNamePlural, filters: { ...filters, ...systemFilters } }">
            {{ verboseNamePlural }}
          </slot>
        </v-toolbar-title>
        <v-spacer />
        <slot name="toolbar" v-bind="{ selectedItems, filters: { ...filters, ...systemFilters } }"></slot>
        <v-menu v-if="filterComponent" bottom left offset-y>
          <template #activator="{ on: menu }">
            <v-tooltip bottom>
              <template #activator="{ on: tooltip }">
                <v-btn icon :disabled="loading" v-on="{ ...tooltip, ...menu }">
                  <v-badge :value="dialogFilterCount" color="primary" dot overlap>
                    <v-icon>mdi-filter-menu</v-icon>
                  </v-badge>
                </v-btn>
              </template>
              <span>Filtros</span>
            </v-tooltip>
          </template>
          <v-list dense>
            <v-list-item v-if="advancedFilters" @click.stop="openFiltersDialog">
              <v-list-item-icon>
                <v-badge :value="dialogFilterCount" color="primary" :content="dialogFilterCount" overlap>
                  <v-icon>mdi-filter</v-icon>
                </v-badge>
              </v-list-item-icon>
              <v-list-item-title>Filtros avanzados</v-list-item-title>
            </v-list-item>
            <v-list-item @click="setFiltersAndFetch({})">
              <v-list-item-icon>
                <v-icon>mdi-eraser</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Limpiar</v-list-item-title>
            </v-list-item>
            <v-list-item @click.stop="openQuickFilterDialog">
              <v-list-item-icon>
                <v-icon>mdi-filter-plus-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-title>Guardar filtro rápido</v-list-item-title>
            </v-list-item>
            <v-divider class="mt-3 mb-2" />
            <v-subheader class="ml-2">Filtros rápidos</v-subheader>
            <v-list-item v-for="filter in quickFilters" :key="filter.label" @click="applyQuickFilter(filter)">
              <v-list-item-title>{{ filter.label }}</v-list-item-title>
              <v-list-item-action class="my-0">
                <v-btn icon @click.stop="pinQuickFilter(filter)">
                  <v-icon v-if="pinnedQuickFilter === filter.key" color="primary">mdi-pin</v-icon>
                  <v-icon v-else>mdi-pin-outline</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
            <v-list-item v-for="filter in customQuickFilters" :key="filter.label" @click="applyQuickFilter(filter)">
              <v-list-item-title>{{ filter.label }}</v-list-item-title>
              <v-list-item-action class="my-0">
                <v-btn icon @click.stop="deleteQuickFilter(filter)">
                  <v-icon color="error">mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-tooltip bottom>
          <template #activator="{ attrs, on }">
            <v-btn
              v-if="customHeaders"
              icon
              :disabled="loading"
              v-bind="attrs"
              v-on="on"
              @click="$refs.customHeadersDialog.open()"
            >
              <v-icon>mdi-table-eye</v-icon>
            </v-btn>
          </template>
          <span>Columnas visibles</span>
        </v-tooltip>
        <v-tooltip bottom>
          <template #activator="{ attrs, on }">
            <v-btn icon :disabled="loading" v-bind="attrs" v-on="on" @click="fetchTableItems">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </template>
          <span>Refrescar</span>
        </v-tooltip>
      </v-toolbar>

      <div v-if="filterComponent" class="pa-3">
        <component
          :is="filterComponent"
          ref="filterComponent"
          :filters.sync="filters"
          @apply:filters="fetchTableItems(true)"
          @change:advanced-filters-count="dialogFilterCount = $event"
        />
      </div>

      <ItemTable
        ref="itemTable"
        v-model="selectedItems"
        :headers="tableHeaders"
        :options.sync="tableOptions"
        :footer-props="tableFooterProps"
        :service="service"
        :filters="filters"
        :system-filters="systemFilters"
        :reactive-filters="reactiveFilters"
        :show-select="selectableRows"
        :elevation="0"
        v-on="$listeners"
      >
        <template #top>
          <slot name="top"></slot>
        </template>

        <template v-for="header in tableAvailableHeaders" #[`item.${header.value}`]="slotProps">
          <slot :name="`item.${header.value}`" v-bind="slotProps"></slot>
        </template>

        <template #item.table_actions="slotProps">
          <span class="d-inline-flex">
            <slot name="item.table_actions" v-bind="slotProps"></slot>
            <template v-if="!readOnly">
              <v-tooltip v-if="canEdit(slotProps.item, loggedUser)" bottom>
                <template #activator="{ on, attrs }">
                  <v-btn icon v-bind="attrs" :disabled="loading" @click.stop="openFormDialog(slotProps.item)" v-on="on">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span> Editar </span>
              </v-tooltip>
              <v-tooltip v-if="canDelete(slotProps.item, loggedUser)" bottom>
                <template #activator="{ on, attrs }">
                  <v-btn
                    icon
                    v-bind="attrs"
                    :disabled="loading"
                    @click.stop="openDeleteDialog(slotProps.item)"
                    v-on="on"
                  >
                    <v-icon>mdi-delete</v-icon>
                  </v-btn>
                </template>
                <span> Eliminar </span>
              </v-tooltip>
            </template>
          </span>
        </template>
      </ItemTable>
    </v-card>

    <TableHeadersConfigDialog
      v-if="customHeaders"
      ref="customHeadersDialog"
      :available-headers="tableAvailableHeaders"
      :headers.sync="tableHeaders"
    />

    <QuickFilterDialog
      ref="quickFilterDialog"
      :quick-filters="customQuickFilters"
      @add:quick-filter="addQuickFilter($event)"
    />

    <slot name="fab" v-bind="{ canCreate, canEdit, canDelete, selectedItems }">
      <v-btn
        v-if="!readOnly && canCreate(loggedUser)"
        fab
        fixed
        bottom
        right
        color="secondary"
        @click.stop="openFormDialog(null)"
      >
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </slot>

    <template v-if="!readOnly">
      <FormDialog
        v-if="formComponent"
        ref="formDialog"
        :verbose-name="verboseName"
        :form-component="formComponent"
        :multi-add="formDialogMultiAdd"
        @submit="onFormSubmit"
      />

      <DeletionConfirmationDialog
        ref="deleteDialog"
        :item-text="itemText"
        :delete-child-items-warning="deleteChildItemsWarning"
        @confirm="deleteItem"
      />
    </template>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { isObject, omit } from "lodash";

import useLocalStorage from "@/composables/useLocalStorage";
import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "ItemIndex",
  props: {
    localStorageNamespace: {
      type: String,
      required: true,
    },
    verboseName: {
      type: String,
      required: true,
    },
    verboseNamePlural: {
      type: String,
      required: true,
    },
    itemText: {
      type: [String, Function],
      default: "name",
    },
    service: {
      type: Object,
      required: true,
    },
    tableAvailableHeaders: {
      type: Array,
      required: true,
    },
    tableInitialOptions: {
      type: Object,
      required: true,
    },
    tableFooterProps: {
      type: Object,
      default: () => ({
        itemsPerPageOptions: [10, 25, 50],
      }),
    },
    formComponent: {
      type: Object,
      default: () => ({}),
    },
    defaultItem: {
      type: Object,
      default: () => ({}),
    },
    deleteChildItemsWarning: {
      type: Boolean,
      default: false,
    },
    canCreate: {
      type: Function,
      default: (user) => user.is_superuser,
    },
    canEdit: {
      type: Function,
      default: (item, user) => user.is_superuser,
    },
    canDelete: {
      type: Function,
      default: (item, user) => user.is_superuser,
    },
    readOnly: {
      type: Boolean,
      default: false,
    },
    filterComponent: {
      type: Object,
      default: undefined,
    },
    systemFilters: {
      type: Object,
      default: () => ({}),
    },
    quickFilters: {
      type: Array,
      default: () => [],
    },
    defaultQuickFilter: {
      type: String,
      default: undefined,
    },
    reactiveFilters: {
      type: Boolean,
      default: false,
    },
    advancedFilters: {
      type: Boolean,
      default: false,
    },
    customHeaders: {
      type: Boolean,
      default: false,
    },
    selectableRows: {
      type: Boolean,
      default: false,
    },
    formDialogMultiAdd: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const localTableOptions = { ...defaultTableOptions, ...props.tableInitialOptions };
    const tableOptions = useLocalStorage(`${props.localStorageNamespace}TableOptions`, localTableOptions, {
      getter: (lsOptions) => ({ ...localTableOptions, ...lsOptions }),
      setter: (options) => omit(options, ["page"]),
    });

    const defaultTableHeaders = props.tableAvailableHeaders.filter((header) => header.default || header.fixed);
    const tableHeaders = useLocalStorage(`${props.localStorageNamespace}TableHeaders`, defaultTableHeaders, {
      getter: (lsHeaders) => props.tableAvailableHeaders.filter((header) => lsHeaders.includes(header.value)),
      setter: (headers) => headers.map((header) => header.value),
    });

    const pinnedQuickFilter = useLocalStorage(
      `${props.localStorageNamespace}PinnedQuickFilter`,
      props.defaultQuickFilter
    );
    const customQuickFilters = useLocalStorage(`${props.localStorageNamespace}QuickFilters`, []);

    return {
      tableHeaders,
      tableOptions,
      pinnedQuickFilter,
      customQuickFilters,
    };
  },
  data() {
    return {
      filters: {},
      dialogFilterCount: 0,
      selectedItems: [],
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["loading"]),
  },
  watch: {
    tableHeaders: {
      handler(newValue) {
        const flatHeaders = newValue.map((header) => header.value);
        const sortingConfig = { sortBy: [], sortDesc: [] };
        this.tableOptions.sortBy.forEach((field, index) => {
          if (flatHeaders.includes(field)) {
            sortingConfig.sortBy.push(field);
            sortingConfig.sortDesc.push(this.tableOptions.sortDesc[index]);
          }
        });
        this.tableOptions = { ...this.tableOptions, ...sortingConfig };
      },
      deep: true,
    },
  },
  created() {
    this.filters = this.getDefaultFilters();
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    fetchTableItems(resetPagination = false) {
      this.$refs.itemTable.fetchItems(resetPagination);
    },
    getDefaultFilters() {
      if (!this.pinnedQuickFilter) {
        return {};
      }
      const defaultFilter = this.quickFilters.find((filter) => filter.key === this.pinnedQuickFilter);
      return defaultFilter ? defaultFilter.filters : {};
    },
    openFiltersDialog() {
      this.$refs.filterComponent.openFiltersDialog();
    },
    addFilter(filter) {
      this.filters = { ...this.filters, ...filter };
    },
    setFiltersAndFetch(filters) {
      this.filters = filters;
      if (!this.reactiveFilters) {
        this.$nextTick(() => {
          this.fetchTableItems(true);
        });
      }
    },
    openQuickFilterDialog() {
      this.$refs.quickFilterDialog.open();
    },
    closeQuickFilterDialog() {
      this.$refs.quickFilterDialog.close();
    },
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
    applyQuickFilter(filter) {
      this.setFiltersAndFetch(filter.filters);
    },
    pinQuickFilter(filter) {
      this.pinnedQuickFilter = filter.key;
      this.showSnackbar({ message: `Se ha fijado el filtro "${filter.label}"` });
    },
    deleteQuickFilter(filter) {
      this.customQuickFilters = this.customQuickFilters.filter((item) => item.label !== filter.label);
      this.showSnackbar({
        color: "success",
        message: "Filtro eliminado correctamente",
      });
    },
    async openFormDialog(item) {
      if (!item) {
        this.$refs.formDialog.open(this.defaultItem);
      } else {
        const response = await this.service.retrieve(item.id);
        this.$refs.formDialog.open(response.data);
      }
    },
    onFormSubmit(item) {
      this.fetchTableItems();
      this.$emit("submit:form", item);
    },
    openDeleteDialog(item) {
      this.$refs.deleteDialog.open(item);
    },
    async deleteItem(item) {
      await this.service.delete(item.id);
      this.fetchTableItems();
      this.$emit("delete:item", item);
      this.showSnackbar({
        color: "success",
        message: "Elemento eliminado correctamente",
      });
    },
  },
};
</script>
