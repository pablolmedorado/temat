<template>
  <v-autocomplete
    v-bind="{ ...$props, ...$attrs }"
    :items="options"
    :loading="isLoading"
    :filter="optionsFilter"
    :search-input.sync="searchInput"
    hide-no-data
    v-on="$listeners"
  >
    <template #append>
      <slot name="append"></slot>
    </template>
    <template #append-outer>
      <slot name="append-outer"></slot>
    </template>
  </v-autocomplete>
</template>

<script>
import { ref, watch } from "@vue/composition-api";
import { debounce, isObject } from "lodash-es";

import { useLoading } from "@/composables/loading";

import { normalize } from "@/utils/text";

export default {
  name: "AsyncAutocomplete",
  inheritAttrs: false,
  props: {
    value: {
      type: [String, Object],
      default: null,
    },
    service: {
      type: Object,
      required: true,
    },
    searchFunctionName: {
      type: String,
      default: "list",
    },
    searchField: {
      type: String,
      default: "search",
    },
    searchLookup: {
      type: String,
      default: "",
    },
    getFunctionName: {
      type: String,
      default: "retrieve",
    },
    itemText: {
      type: [String, Array, Function],
      default: "name",
    },
    itemValue: {
      type: [String, Array, Function],
      default: "id",
    },
    returnObject: {
      type: Boolean,
      default: false,
    },
    clearable: {
      type: Boolean,
      default: true,
    },
    placeholder: {
      type: String,
      default: "Escribe para iniciar la búsqueda...",
    },
  },
  setup(props, { emit }) {
    // Composables
    const { isLoading, addTask, removeTask, isTaskLoading } = useLoading();

    // Options
    const options = ref([]);
    function optionsFilter(item, queryText, itemText) {
      const normalizedQueryText = normalize(queryText).toLowerCase();
      const normalizedItemText = normalize(itemText).toLowerCase();
      return normalizedItemText.includes(normalizedQueryText);
    }

    // Search
    const searchInput = ref(null);
    const search = debounce(async (query) => {
      addTask("search");
      try {
        const requestParams = { page_size: 15, page: 1 };
        const lookup = props.searchLookup ? `__${props.searchLookup}` : "";
        const searchParam = `${props.searchField}${lookup}`;
        requestParams[searchParam] = query;

        const response = await props.service[props.searchFunctionName](requestParams);
        options.value = response.data.results;
      } finally {
        removeTask("search");
      }
    }, 200);
    watch(searchInput, (newValue) => {
      if (newValue) {
        if (isTaskLoading("search")) {
          return;
        }
        const exactMatch = options.value.find((item) => newValue.toLowerCase() === item[props.itemText].toLowerCase());
        if (!exactMatch) {
          search(newValue);
        }
      } else {
        options.value = [];
      }
    });

    // Watchers
    watch(
      () => props.value,
      async (newValue, oldValue) => {
        if (newValue) {
          const newValueId = isObject(newValue) ? newValue[props.itemValue] : newValue;
          const oldValueId = isObject(oldValue) ? oldValue[props.itemValue] : oldValue;
          if (newValueId == oldValueId) {
            if (props.returnObject && !isObject(newValue) && isObject(oldValue)) {
              emit("input", oldValue);
            }
          } else {
            if (isObject(newValue)) {
              options.value = [newValue];
            } else {
              addTask("fetch-item");
              try {
                const response = await props.service[props.getFunctionName](newValueId);
                options.value = [response.data];
                if (props.returnObject) {
                  emit("input", response.data);
                }
              } finally {
                removeTask("fetch-item");
              }
            }
          }
        }
      },
      { immediate: true }
    );

    return {
      isLoading,
      // Options
      options,
      optionsFilter,
      // Search
      searchInput,
    };
  },
};
</script>

<style scoped>
.db-icon {
  cursor: help;
  opacity: 0.6;
}
</style>
