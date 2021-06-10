<template>
  <v-autocomplete
    v-bind="{ ...$props, ...$attrs }"
    :items="options"
    :loading="isLoading"
    :filter="filter"
    :search-input.sync="searchInput"
    hide-no-data
    v-on="$listeners"
  >
    <template #append>
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <v-icon v-bind="attrs" class="db-icon" v-on="on">mdi-database-search-outline</v-icon>
        </template>
        <span> Realiza búsqueda en BD </span>
      </v-tooltip>
    </template>
  </v-autocomplete>
</template>

<script>
import { debounce, isObject } from "lodash";

import useLoading from "@/composables/useLoading";

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
  setup() {
    const { isLoading, addTask, removeTask, isTaskLoading } = useLoading();
    return {
      isLoading,
      addTask,
      removeTask,
      isTaskLoading,
    };
  },
  data() {
    return {
      options: [],
      searchInput: null,
    };
  },
  watch: {
    value: {
      async handler(newValue, oldValue) {
        if (newValue) {
          const newValueId = isObject(newValue) ? newValue[this.itemValue] : newValue;
          const oldValueId = isObject(oldValue) ? oldValue[this.itemValue] : oldValue;
          if (newValueId == oldValueId) {
            if (this.returnObject && !isObject(newValue) && isObject(oldValue)) {
              this.$emit("input", oldValue);
            }
          } else {
            if (isObject(newValue)) {
              this.options = [newValue];
            } else {
              this.addTask("fetch-item");
              try {
                const response = await this.service[this.getFunctionName](newValueId);
                this.options = [response.data];
                if (this.returnObject) {
                  this.$emit("input", response.data);
                }
              } finally {
                this.removeTask("fetch-item");
              }
            }
          }
        }
      },
      immediate: true,
    },
    searchInput(newValue) {
      if (newValue) {
        if (this.isTaskLoading("search")) {
          return;
        }
        const exactMatch = this.options.find((item) => newValue.toLowerCase() === item[this.itemText].toLowerCase());
        if (!exactMatch) {
          this.debouncedSearch(newValue);
        }
      } else {
        this.options = [];
      }
    },
  },
  methods: {
    async search(query) {
      this.addTask("search");
      try {
        const requestParams = { page_size: 15, page: 1 };
        const lookup = this.searchLookup ? `__${this.searchLookup}` : "";
        const searchParam = `${this.searchField}${lookup}`;
        requestParams[searchParam] = query;

        const response = await this.service[this.searchFunctionName](requestParams);
        this.options = response.data.results;
      } finally {
        this.removeTask("search");
      }
    },
    debouncedSearch: debounce(function (query) {
      this.search(query);
    }, 200),
    normalizeText(text) {
      return text.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    },
    filter(item, queryText, itemText) {
      const normalizedQueryText = this.normalizeText(queryText).toLowerCase();
      const normalizedItemText = this.normalizeText(itemText).toLowerCase();
      return normalizedItemText.includes(normalizedQueryText);
    },
  },
};
</script>

<style scoped>
.db-icon {
  cursor: help;
  opacity: 0.6;
}
</style>
