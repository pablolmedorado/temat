import { get } from "lodash";

export default {
  props: {
    filters: {
      type: Object,
      default: () => ({}),
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      showFiltersDialog: false,
      basicFilters: [],
    };
  },
  watch: {
    filters: {
      handler(newValue) {
        if (this.basicFilters.length) {
          const advancedFilterCount = Object.entries(newValue).filter(
            (filter) => filter[1] && !this.basicFilters.includes(filter[0])
          ).length;
          this.$emit("change:advanced-filters-count", advancedFilterCount);
        }
      },
      deep: true,
      immediate: true,
    },
  },
  methods: {
    updateFilters(filter) {
      this.$emit("update:filters", { ...this.filters, ...filter });
    },
    clearFilters() {
      this.$emit("update:filters", {});
    },
    openFiltersDialog() {
      this.showFiltersDialog = true;
    },
    closeFiltersDialog() {
      this.showFiltersDialog = false;
    },
    applyFiltersFromDialog() {
      this.$emit("apply:filters");
      this.closeFiltersDialog();
    },
    splitFilterValue(field, isInteger) {
      const filterValue = get(this.filters, field);
      if (!filterValue) {
        return [];
      }
      const splittedValues = filterValue.split(",");
      if (isInteger) {
        return splittedValues.map((item) => parseInt(item));
      }
      return splittedValues;
    },
  },
};
