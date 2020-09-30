<template>
  <div>
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          <slot name="title" v-bind="{ verboseName, verboseNamePlural, filters }">
            {{ verboseNamePlural }}
          </slot>
        </v-toolbar-title>
        <v-spacer></v-spacer>
        <slot name="toolbar" v-bind="{ selectedItems, filters }"></slot>
        <template v-if="advancedFilters">
          <v-tooltip bottom>
            <template v-slot:activator="{ attrs, on }">
              <v-btn icon v-bind="attrs" v-on="on" @click="resetFilters">
                <v-icon>mdi-filter-remove-outline</v-icon>
              </v-btn>
            </template>
            <span>Limpiar filtros</span>
          </v-tooltip>
          <v-tooltip bottom>
            <template v-slot:activator="{ attrs, on }">
              <v-btn icon v-bind="attrs" v-on="on" @click.stop="openFiltersDialog">
                <v-badge :value="dialogFilterCount" color="primary" :content="dialogFilterCount" overlap>
                  <v-icon>mdi-filter</v-icon>
                </v-badge>
              </v-btn>
            </template>
            <span>Filtros avanzados</span>
          </v-tooltip>
        </template>
        <v-tooltip bottom>
          <template v-slot:activator="{ attrs, on }">
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
          <template v-slot:activator="{ attrs, on }">
            <v-btn icon :disabled="loading" v-bind="attrs" v-on="on" @click="fetchTableItems">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </template>
          <span>Refrescar</span>
        </v-tooltip>
      </v-toolbar>

      <component
        :is="filterComponent"
        v-if="filterComponent"
        ref="filterComponent"
        :filters.sync="filters"
        @reset:filters="resetFilters"
        @apply:filters="fetchTableItems(true)"
        @change:advanced-filters-count="dialogFilterCount = $event"
      />

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
        <template v-slot:top>
          <slot name="top"></slot>
        </template>

        <template v-for="header in tableAvailableHeaders" v-slot:[`item.${header.value}`]="slotProps">
          <slot :name="`item.${header.value}`" v-bind="slotProps">
            {{ slotProps.value }}
          </slot>
        </template>

        <template v-slot:item.table_actions="slotProps">
          <span class="d-inline-flex">
            <slot name="item.table_actions" v-bind="slotProps"></slot>
            <template v-if="!readOnly">
              <v-tooltip v-if="canEdit(slotProps.item, loggedUser)" bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn icon v-bind="attrs" :disabled="loading" @click.stop="openFormDialog(slotProps.item)" v-on="on">
                    <v-icon>mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>
                  Editar
                </span>
              </v-tooltip>
              <v-tooltip v-if="canDelete(slotProps.item, loggedUser)" bottom>
                <template v-slot:activator="{ on, attrs }">
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
                <span>
                  Eliminar
                </span>
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

    <template v-if="!readOnly">
      <slot name="fab" v-bind="{ canCreate, canEdit, canDelete }">
        <v-btn v-if="canCreate(loggedUser)" fab fixed bottom right color="secondary" @click.stop="openFormDialog(null)">
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </slot>

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
import { omit } from "lodash";

import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "ItemIndex",
  props: {
    localStorageKey: {
      type: String,
      required: true
    },
    verboseName: {
      type: String,
      required: true
    },
    verboseNamePlural: {
      type: String,
      required: true
    },
    itemText: {
      type: [String, Function],
      default: "name"
    },
    service: {
      type: Function,
      required: true
    },
    tableAvailableHeaders: {
      type: Array,
      required: true
    },
    tableInitialOptions: {
      type: Object,
      required: true
    },
    tableFooterProps: {
      type: Object,
      default: () => ({
        itemsPerPageOptions: [10, 25, 50]
      })
    },
    formComponent: {
      type: Object,
      default: () => ({})
    },
    defaultItem: {
      type: Object,
      default: () => ({})
    },
    deleteChildItemsWarning: {
      type: Boolean,
      default: false
    },
    canCreate: {
      type: Function,
      default: user => user.is_staff
    },
    canEdit: {
      type: Function,
      default: (item, user) => user.is_staff
    },
    canDelete: {
      type: Function,
      default: (item, user) => user.is_staff
    },
    readOnly: {
      type: Boolean,
      default: false
    },
    filterComponent: {
      type: Object,
      default: undefined
    },
    systemFilters: {
      type: Object,
      default: () => ({})
    },
    defaultFilters: {
      type: Object,
      default: () => ({})
    },
    reactiveFilters: {
      type: Boolean,
      default: false
    },
    advancedFilters: {
      type: Boolean,
      default: false
    },
    customHeaders: {
      type: Boolean,
      default: false
    },
    selectableRows: {
      type: Boolean,
      default: false
    },
    formDialogMultiAdd: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      tableHeaders: null,
      tableOptions: null,
      filters: {},
      dialogFilterCount: 0,
      selectedItems: []
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["loading"])
  },
  watch: {
    tableHeaders: {
      handler(newValue) {
        const flatHeaders = newValue.map(header => header.value);
        localStorage[`${this.localStorageKey}TableHeaders`] = JSON.stringify(flatHeaders);

        const sortingConfig = { sortBy: [], sortDesc: [] };
        this.tableOptions.sortBy.forEach((field, index) => {
          if (flatHeaders.includes(field)) {
            sortingConfig.sortBy.push(field);
            sortingConfig.sortDesc.push(this.tableOptions.sortDesc[index]);
          }
        });
        this.tableOptions = { ...this.tableOptions, ...sortingConfig };
      },
      deep: true
    },
    tableOptions: {
      handler(newValue) {
        localStorage[`${this.localStorageKey}TableOptions`] = JSON.stringify(omit(newValue, ["page"]));
      },
      deep: true
    },
    defaultFilters: {
      handler(newValue) {
        this.filters = newValue;
      },
      deep: true,
      immediate: true
    }
  },
  created() {
    this.loadOptionsFromLocalStorage();
    this.loadHeadersFromLocalStorage();
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    fetchTableItems(resetPagination = false) {
      this.$refs.itemTable.fetchItems(resetPagination);
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
        message: "Elemento eliminado correctamente"
      });
    },
    openFiltersDialog() {
      this.$refs.filterComponent.openFiltersDialog();
    },
    addFilter(filter) {
      this.filters = { ...this.filters, ...filter };
    },
    resetFilters() {
      this.filters = this.defaultFilters;
      if (!this.reactiveFilters) {
        this.$nextTick(() => {
          this.fetchTableItems(true);
        });
      }
    },
    loadHeadersFromLocalStorage() {
      const lsTableHeaders = localStorage[`${this.localStorageKey}TableHeaders`];
      if (lsTableHeaders) {
        this.tableHeaders = this.tableAvailableHeaders.filter(header => lsTableHeaders.includes(header.value));
      } else {
        this.tableHeaders = this.tableAvailableHeaders.filter(header => header.default || header.fixed);
      }
    },
    loadOptionsFromLocalStorage() {
      const localOptions = { ...defaultTableOptions, ...this.tableInitialOptions };
      const lsTableOptions = localStorage[`${this.localStorageKey}TableOptions`];
      this.tableOptions = lsTableOptions ? { ...localOptions, ...JSON.parse(lsTableOptions) } : localOptions;
    }
  }
};
</script>
