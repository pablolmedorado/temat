<template>
  <v-data-table
    v-if="headers.length"
    v-bind="$attrs"
    :value="value"
    :headers="headers"
    :options="options"
    :footer-props="footerProps"
    :items="items"
    :item-key="itemKey"
    :server-items-length="itemCount"
    :loading="tableLoading"
    :no-data-text="noDataText"
    :class="[`elevation-${elevation}`]"
    v-on="$listeners"
  >
    <template #top="props">
      <slot name="top" v-bind="props"></slot>
    </template>

    <template v-for="header in headers" #[`item.${header.value}`]="item">
      <slot :name="`item.${header.value}`" v-bind="item">
        {{ item.value }}
      </slot>
    </template>
  </v-data-table>
</template>

<script>
import { defaultTo, isEqual, uniq } from "lodash";

import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "ItemTable",
  inheritAttrs: false,
  props: {
    value: {
      type: Array,
      default: () => [],
    },
    service: {
      type: Object,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
    options: {
      type: Object,
      default: () => defaultTableOptions,
    },
    footerProps: {
      type: Object,
      default: () => ({
        itemsPerPageOptions: [10, 25, 50],
      }),
    },
    filters: {
      type: Object,
      default: () => ({}),
    },
    systemFilters: {
      type: Object,
      default: () => ({}),
    },
    reactiveFilters: {
      type: Boolean,
      default: false,
    },
    itemKey: {
      type: String,
      default: "id",
    },
    noDataText: {
      type: String,
      default: "No hay elementos coincidentes con los filtros aplicados",
    },
    elevation: {
      type: Number,
      default: 2,
    },
  },
  data() {
    return {
      tableLoading: true,
      items: [],
      itemCount: 0,
      resetPagination: false,
    };
  },
  computed: {
    fields() {
      let fields = [this.itemKey];
      this.headers.forEach((header) => {
        if (header.fields) {
          fields = [...fields, ...header.fields];
        } else if (header.value !== "table_actions") {
          fields.push(header.value);
        }
      });
      return uniq(fields);
    },
    expand() {
      const expand = [];
      this.fields.forEach((field) => {
        const splittedField = field.split(".");
        if (splittedField.length > 1) {
          expand.push(splittedField.slice(0, splittedField.length - 1).join("."));
        }
      });
      return uniq(expand);
    },
    ordering() {
      const ordering = [];
      this.options.sortBy.forEach((field, index) => {
        const header = this.headers.find((header) => header.value === field);
        if (header) {
          ordering.push(`${this.options.sortDesc[index] ? "-" : ""}${defaultTo(header.sortingField, field)}`);
        }
      });
      return ordering;
    },
  },
  watch: {
    filters: {
      handler() {
        if (this.reactiveFilters) {
          this.fetchItems(true);
        }
      },
      deep: true,
    },
    options: {
      handler(newValue, oldValue) {
        if (!isEqual(newValue, oldValue)) {
          this.fetchItems();
        }
      },
      deep: true,
    },
    headers: {
      handler(newValue, oldValue) {
        if (!isEqual(newValue, oldValue)) {
          this.fetchItems();
        }
      },
      deep: true,
    },
  },
  activated() {
    if (this.headers.length) {
      this.fetchItems();
    }
  },
  methods: {
    buildFetchRequestParams() {
      return {
        ...this.filters,
        ...this.systemFilters,
        fields: this.fields.join(","),
        expand: this.expand.join(","),
        ordering: this.ordering.join(","),
        page: this.options.page,
        page_size: this.options.itemsPerPage,
      };
    },
    async fetchItems(resetPagination = false) {
      if (resetPagination && this.options.page !== 1) {
        this.$emit("update:options", { ...this.options, page: 1 });
      } else {
        this.tableLoading = true;
        try {
          this.$emit("input", []);
          const response = await this.service.list(this.buildFetchRequestParams());
          this.items = this.options.itemsPerPage <= 0 ? response.data : response.data.results;
          this.itemCount = this.options.itemsPerPage <= 0 ? response.data.length : response.data.count;
        } finally {
          this.tableLoading = false;
        }
      }
    },
  },
};
</script>
