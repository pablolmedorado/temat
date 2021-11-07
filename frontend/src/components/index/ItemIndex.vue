<template>
  <div>
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          <slot
            name="title"
            v-bind="{
              verboseName: modelClass.verboseName,
              verboseNamePlural: modelClass.verboseNamePlural,
              filters: { ...filters, ...systemFilters },
            }"
          >
            {{ modelClass.verboseNamePlural }}
          </slot>
        </v-toolbar-title>
        <v-spacer />
        <slot
          name="toolbar"
          v-bind="{
            selectedItems,
            filters: { ...filters, ...systemFilters },
            isTableLoading: isChildLoading('itemTable'),
            isIndexLoading: isLoading,
          }"
        ></slot>
        <FilterManager
          v-if="filterComponent"
          :local-storage-namespace="lsNamespace"
          :filters="filters"
          :advanced-filters="advancedFilters"
          :advanced-filters-count="dialogFilterCount"
          :quick-filters="quickFilters"
          :default-quick-filter="defaultQuickFilter"
          :pinned-quick-filter.sync="pinnedQuickFilter"
          :disabled="isChildLoading('itemTable')"
          @clear:filters="setFiltersAndFetch({})"
          @open:config-dialog="$refs.filterComponent.openFiltersDialog()"
          @apply:filter="applyQuickFilter"
        />
        <TableHeaderManager
          v-if="customHeaders"
          :available-headers="tableAvailableHeaders"
          :headers.sync="tableHeaders"
          :disabled="isChildLoading('itemTable')"
        />
        <v-tooltip bottom>
          <template #activator="{ attrs, on }">
            <v-btn icon :disabled="isChildLoading('itemTable')" v-bind="attrs" v-on="on" @click="fetchTableItems">
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
          :disabled="isChildLoading('itemTable')"
          @hook:mounted="advancedFilters = $refs.filterComponent.hasAdvancedFilters"
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
        <template #top="slotProps">
          <slot name="top" v-bind="{ ...slotProps, isIndexLoading: isLoading }"></slot>
        </template>

        <template v-for="header in tableAvailableHeaders" #[`item.${header.value}`]="slotProps">
          <slot :name="`item.${header.value}`" v-bind="{ ...slotProps, isIndexLoading: isLoading }"></slot>
        </template>

        <template #item.table_actions="slotProps">
          <span class="d-inline-flex">
            <slot name="item.table_actions" v-bind="{ ...slotProps, isIndexLoading: isLoading }"></slot>
            <v-tooltip v-if="canChangeItem(slotProps.item) && formComponent" bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  v-bind="attrs"
                  :disabled="isLoading || disableRowEdition"
                  :loading="isTaskLoading('fetch-item', slotProps.item.id)"
                  @click.stop="openFormDialog(slotProps.item)"
                  v-on="on"
                >
                  <v-icon>mdi-pencil</v-icon>
                </v-btn>
              </template>
              <span> Editar </span>
            </v-tooltip>
            <v-tooltip v-if="canDeleteItem(slotProps.item)" bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  v-bind="attrs"
                  :disabled="isLoading || disableRowEdition"
                  :loading="isTaskLoading('delete-item', slotProps.item.id)"
                  @click.stop="$refs.deleteDialog.open(slotProps.item)"
                  v-on="on"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span> Eliminar </span>
            </v-tooltip>
          </span>
        </template>
      </ItemTable>
    </v-card>

    <slot name="fab" v-bind="{ canAddItems, selectedItems }">
      <v-btn
        v-if="formComponent && canAddItems()"
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

    <FormDialog
      v-if="formComponent"
      ref="formDialog"
      :verbose-name="modelClass.verboseName"
      :form-component="formComponent"
      :multi-add="formDialogMultiAdd"
      @submit="onFormSubmit"
    />

    <DeletionConfirmationDialog
      ref="deleteDialog"
      :item-text="modelClass.itemText"
      :delete-child-items-warning="deleteChildItemsWarning"
      @confirm="deleteItem"
    />
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
import { defaultTo, get, invoke, isBoolean, isFunction, omit } from "lodash";

import useLoading from "@/composables/useLoading";
import useLocalStorage from "@/composables/useLocalStorage";
import { defaultTableOptions } from "@/utils/constants";
import { getServiceByBasename } from "@/services";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "ItemIndex",
  provide() {
    return {
      indexModelClass: this.modelClass,
    };
  },
  props: {
    modelClass: {
      type: Function,
      required: true,
    },
    localStorageNamespace: {
      type: String,
      default: undefined,
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
      default: undefined,
    },
    defaultItem: {
      type: Object,
      default: undefined,
    },
    deleteChildItemsWarning: {
      type: Boolean,
      default: false,
    },
    allowAdd: {
      type: [Boolean, String, Function],
      default: false,
    },
    allowChange: {
      type: [Boolean, String, Function],
      default: false,
    },
    allowDelete: {
      type: [Boolean, String, Function],
      default: false,
    },
    disableRowEdition: {
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
    const { isLoading, isChildLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemTable"],
    });

    const lsNamespace = defaultTo(props.localStorageNamespace, props.modelClass.localStorageNamespace);

    const localTableOptions = { ...defaultTableOptions, ...props.tableInitialOptions };
    const tableOptions = useLocalStorage(`${lsNamespace}TableOptions`, localTableOptions, {
      getter: (lsOptions) => ({ ...localTableOptions, ...lsOptions }),
      setter: (options) => omit(options, ["page"]),
    });

    const defaultTableHeaders = props.tableAvailableHeaders.filter((header) => header.default || header.fixed);
    const tableHeaders = useLocalStorage(`${lsNamespace}TableHeaders`, defaultTableHeaders, {
      getter: (lsHeaders) => props.tableAvailableHeaders.filter((header) => lsHeaders.includes(header.value)),
      setter: (headers) => headers.map((header) => header.value),
    });

    const pinnedQuickFilter = useLocalStorage(`${lsNamespace}PinnedQuickFilter`, props.defaultQuickFilter);

    return {
      isLoading,
      isChildLoading,
      isTaskLoading,
      addTask,
      removeTask,
      lsNamespace,
      tableHeaders,
      tableOptions,
      pinnedQuickFilter,
    };
  },
  data() {
    return {
      service: getServiceByBasename(this.modelClass.serviceBasename),
      filters: {},
      advancedFilters: false,
      dialogFilterCount: 0,
      selectedItems: [],
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
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
      invoke(this.$refs.itemTable, "fetchItems", resetPagination);
    },
    getDefaultFilters() {
      if (!this.pinnedQuickFilter) {
        return {};
      }
      const defaultFilter = this.quickFilters.find((filter) => filter.key === this.pinnedQuickFilter);
      return get(defaultFilter, "filters", {});
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
    applyQuickFilter(filter) {
      this.setFiltersAndFetch(filter.filters);
    },
    canAddItems() {
      return this.checkPermission(this.allowAdd);
    },
    canChangeItem(item) {
      return this.checkPermission(this.allowChange, item);
    },
    canDeleteItem(item) {
      return this.checkPermission(this.allowDelete, item);
    },
    checkPermission(permission, item) {
      if (isBoolean(permission)) {
        return permission;
      }
      return isFunction(permission) ? permission(this.loggedUser, item) : userHasPermission(permission);
    },
    async openFormDialog(item) {
      if (!item) {
        const newItem = defaultTo(this.defaultItem, this.modelClass.defaults);
        this.$refs.formDialog.open(newItem);
      } else {
        this.addTask("fetch-item", item.id);
        try {
          const response = await this.service.retrieve(item.id);
          this.$refs.formDialog.open(response.data);
        } finally {
          this.removeTask("fetch-item", item.id);
        }
      }
    },
    onFormSubmit(item) {
      this.fetchTableItems();
      this.$emit("submit:form", item);
    },
    async deleteItem(item) {
      this.addTask("delete-item", item.id);
      try {
        await this.service.delete(item.id);
        this.$emit("delete:item", item);
        this.fetchTableItems();
        this.showSnackbar({
          color: "success",
          message: "Elemento eliminado correctamente",
        });
      } finally {
        this.removeTask("delete-item", item.id);
      }
    },
  },
};
</script>
