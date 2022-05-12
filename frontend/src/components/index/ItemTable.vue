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
    :loading="isLoading"
    :no-data-text="noDataText"
    :class="[`elevation-${elevation}`]"
    v-on="$listeners"
  >
    <template #top="slotProps">
      <slot name="top" v-bind="{ ...slotProps, isTableLoading: isLoading }"></slot>
    </template>

    <template v-for="header in headers" #[`item.${header.value}`]="slotProps">
      <slot :name="`item.${header.value}`" v-bind="{ ...slotProps, isTableLoading: isLoading }">
        {{ slotProps.value }}
      </slot>
    </template>
  </v-data-table>
</template>

<script>
import { computed, onActivated, ref, watch } from "@vue/composition-api";
import { defaultTo, isEqual, uniq } from "lodash-es";

import { useLoading } from "@/composables/loading";
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
  setup(props, { emit }) {
    // Composables
    const { isLoading, addTask, removeTask } = useLoading();

    // State
    const items = ref([]);
    const itemCount = ref(0);

    // Computed
    const fields = computed(() => {
      let fields = [props.itemKey];
      props.headers.forEach((header) => {
        if (header.fields) {
          fields = [...fields, ...header.fields];
        } else if (header.value !== "table_actions") {
          fields.push(header.value);
        }
      });
      return uniq(fields);
    });
    const expand = computed(() => {
      const expand = [];
      fields.value.forEach((field) => {
        const splittedField = field.split(".");
        if (splittedField.length > 1) {
          expand.push(splittedField.slice(0, splittedField.length - 1).join("."));
        }
      });
      return uniq(expand);
    });
    const ordering = computed(() => {
      const ordering = [];
      props.options.sortBy.forEach((field, index) => {
        const header = props.headers.find((header) => header.value === field);
        if (header) {
          ordering.push(`${props.options.sortDesc[index] ? "-" : ""}${defaultTo(header.sortingField, field)}`);
        }
      });
      return ordering;
    });

    // Methods
    async function fetchItems(resetPagination = false) {
      if (resetPagination && props.options.page !== 1) {
        emit("update:options", { ...props.options, page: 1 });
      } else {
        addTask("fetch-items");
        try {
          const response = await props.service.list({
            ...props.filters,
            ...props.systemFilters,
            fields: fields.value.join(","),
            expand: expand.value.join(","),
            ordering: ordering.value.join(","),
            page: props.options.page,
            page_size: props.options.itemsPerPage,
          });
          emit("input", []);
          items.value = props.options.itemsPerPage <= 0 ? response.data : response.data.results;
          itemCount.value = props.options.itemsPerPage <= 0 ? response.data.length : response.data.count;
        } finally {
          removeTask("fetch-items");
        }
      }
    }

    // Watchers
    watch(
      () => props.filters,
      (newValue, oldValue) => {
        if (!isEqual(newValue, oldValue) && props.reactiveFilters) {
          fetchItems(true);
        }
      },
      { deep: true }
    );
    watch(
      () => props.options,
      (newValue, oldValue) => {
        if (!isEqual(newValue, oldValue)) {
          fetchItems(true);
        }
      },
      { deep: true }
    );
    watch(
      () => props.headers,
      (newValue, oldValue) => {
        if (!isEqual(newValue, oldValue)) {
          fetchItems(true);
        }
      },
      { deep: true }
    );

    // Lifecycle hooks
    onActivated(() => {
      if (props.headers.length) {
        fetchItems();
      }
    });

    return {
      // State
      isLoading,
      items,
      itemCount,
      // Methods
      fetchItems,
    };
  },
};
</script>

<style scoped>
.v-data-table ::v-deep .v-data-table-header th {
  white-space: nowrap;
}
</style>
