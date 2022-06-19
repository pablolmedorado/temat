<template>
  <div>
    <v-card :flat="flat" :outlined="outlined">
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
        />
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
      v-if="formComponent && (allowAdd || allowChange)"
      ref="formDialog"
      :verbose-name="modelClass.verboseName"
      :form-component="formComponent"
      :multi-add="formDialogMultiAdd"
      @submit="onFormSubmit"
    />

    <DeletionConfirmationDialog
      v-if="allowDelete"
      ref="deleteDialog"
      :item-text="modelClass.itemText"
      :delete-child-items-warning="deleteChildItemsWarning"
      @confirm="deleteItem"
    />
  </div>
</template>

<script>
import { nextTick, provide, ref, watch } from "@vue/composition-api";
import { useLocalStorage } from "@vueuse/core";
import { defaultTo, get, invoke, isBoolean, isFunction, omit } from "lodash-es";

import { useMainStore } from "@/stores/main";

import { useLoading } from "@/composables/loading";

import { defaultTableOptions } from "@/utils/constants";
import { userHasPermission } from "@/utils/permissions";

import { getServiceByBasename } from "@/services";

export default {
  name: "ItemIndex",
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
    flat: {
      type: Boolean,
      default: false,
    },
    outlined: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit, refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { isLoading, isChildLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemTable"],
    });

    // State
    const service = getServiceByBasename(props.modelClass.serviceBasename);
    const lsNamespace = defaultTo(props.localStorageNamespace, props.modelClass.localStorageNamespace);

    // Table
    const selectedItems = ref([]);
    const localTableOptions = { ...defaultTableOptions, ...props.tableInitialOptions };
    const tableOptions = useLocalStorage(`${lsNamespace}TableOptions`, localTableOptions, {
      serializer: {
        read: (lsOptions) => {
          const options = lsOptions ? JSON.parse(lsOptions) : {};
          return { ...localTableOptions, ...options };
        },
        write: (options) => JSON.stringify(omit(options, ["page"])),
      },
    });
    const defaultTableHeaders = props.tableAvailableHeaders.filter((header) => header.default || header.fixed);
    const tableHeaders = useLocalStorage(`${lsNamespace}TableHeaders`, defaultTableHeaders, {
      serializer: {
        read: (lsHeaders) => {
          const headers = lsHeaders ? JSON.parse(lsHeaders) : [];
          return props.tableAvailableHeaders.filter((header) => headers.includes(header.value));
        },
        write: (headers) => JSON.stringify(headers.map((header) => header.value)),
      },
    });
    watch(
      tableHeaders,
      (newValue) => {
        const flatHeaders = newValue.map((header) => header.value);
        const sortingConfig = { sortBy: [], sortDesc: [] };
        tableOptions.value.sortBy.forEach((field, index) => {
          if (flatHeaders.includes(field)) {
            sortingConfig.sortBy.push(field);
            sortingConfig.sortDesc.push(tableOptions.value.sortDesc[index]);
          }
        });
        tableOptions.value = { ...tableOptions.value, ...sortingConfig };
      },
      { deep: true }
    );
    function fetchTableItems(resetPagination = false) {
      invoke(refs.itemTable, "fetchItems", resetPagination);
    }

    // Filters
    const filters = ref({});
    const pinnedQuickFilter = useLocalStorage(`${lsNamespace}PinnedQuickFilter`, props.defaultQuickFilter);
    const advancedFilters = ref(false);
    const dialogFilterCount = ref(0);
    function getDefaultFilters() {
      if (!pinnedQuickFilter.value) {
        return {};
      }
      const defaultFilter = props.quickFilters.find((filter) => filter.key === pinnedQuickFilter.value);
      return get(defaultFilter, "filters", {});
    }
    function addFilter(newFilter) {
      filters.value = { ...filters.value, ...newFilter };
    }
    function setFiltersAndFetch(newFilters) {
      filters.value = newFilters;
      if (!props.reactiveFilters) {
        nextTick(() => {
          fetchTableItems(true);
        });
      }
    }
    function applyQuickFilter(quickFilter) {
      setFiltersAndFetch(quickFilter.filters);
    }

    // Permissions
    function canAddItems() {
      return checkPermission(props.allowAdd);
    }
    function canChangeItem(item) {
      return checkPermission(props.allowChange, item);
    }
    function canDeleteItem(item) {
      return checkPermission(props.allowDelete, item);
    }
    function checkPermission(permission, item) {
      if (isBoolean(permission)) {
        return permission;
      }
      return isFunction(permission) ? permission(store.currentUser, item) : userHasPermission(permission);
    }

    // Form
    async function openFormDialog(item) {
      if (!item) {
        const newItem = defaultTo(props.defaultItem, props.modelClass.getDefaults());
        refs.formDialog.open(newItem);
      } else {
        addTask("fetch-item", item.id);
        try {
          const response = await service.retrieve(item.id);
          refs.formDialog.open(response.data);
        } finally {
          removeTask("fetch-item", item.id);
        }
      }
    }
    function onFormSubmit(item) {
      fetchTableItems();
      emit("submit:form", item);
    }

    // Item
    async function deleteItem(item) {
      addTask("delete-item", item.id);
      try {
        await service.delete(item.id);
        emit("delete:item", item);
        fetchTableItems();
        store.showSnackbar({
          color: "success",
          message: "Elemento eliminado correctamente",
        });
      } finally {
        removeTask("delete-item", item.id);
      }
    }

    // Dependency injection
    provide("indexModelClass", props.modelClass);

    // Initialization
    filters.value = getDefaultFilters();

    return {
      isLoading,
      isChildLoading,
      isTaskLoading,
      service,
      lsNamespace,
      // Table
      selectedItems,
      tableOptions,
      tableHeaders,
      fetchTableItems,
      // Filters
      filters,
      pinnedQuickFilter,
      advancedFilters,
      dialogFilterCount,
      addFilter,
      setFiltersAndFetch,
      applyQuickFilter,
      // Permissions
      canAddItems,
      canChangeItem,
      canDeleteItem,
      // Form
      openFormDialog,
      onFormSubmit,
      // Item
      deleteItem,
    };
  },
};
</script>
