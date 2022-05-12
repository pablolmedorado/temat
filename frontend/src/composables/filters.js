import { getCurrentInstance, onMounted, ref, watch } from "@vue/composition-api";
import { get, has } from "lodash-es";

export const filterProps = {
  filters: {
    type: Object,
    default: () => ({}),
  },
  disabled: {
    type: Boolean,
    default: false,
  },
};

export function useFilters(options = {}) {
  // Default options
  const { basicFilters = [] } = options;

  // Vue instance
  const { emit, props, refs } = getCurrentInstance();

  // State
  const showFiltersDialog = ref(false);
  const hasAdvancedFilters = ref(false);

  // Watchers
  watch(
    () => props.filters,
    (newValue) => {
      if (basicFilters.length) {
        const advancedFilterCount = Object.entries(newValue).filter(
          (filter) => filter[1] && !basicFilters.includes(filter[0])
        ).length;
        emit("change:advanced-filters-count", advancedFilterCount);
      }
    },
    { deep: true, immediate: true }
  );

  // Methods
  function updateFilters(filter) {
    emit("update:filters", { ...props.filters, ...filter });
  }
  function clearFilters() {
    emit("update:filters", {});
  }
  function openFiltersDialog() {
    showFiltersDialog.value = true;
  }
  function closeFiltersDialog() {
    showFiltersDialog.value = false;
  }
  function applyFiltersFromDialog() {
    emit("apply:filters");
    closeFiltersDialog();
  }
  function splitFilterValue(field, isInteger) {
    const filterValue = get(props.filters, field);
    if (!filterValue) {
      return [];
    }
    const splittedValues = filterValue.split(",");
    if (isInteger) {
      return splittedValues.map((item) => parseInt(item));
    }
    return splittedValues;
  }

  // Lifecycle hooks
  onMounted(() => (hasAdvancedFilters.value = has(refs, "advancedFiltersDialog")));

  return {
    // State
    showFiltersDialog,
    hasAdvancedFilters,
    // Methods
    updateFilters,
    clearFilters,
    openFiltersDialog,
    closeFiltersDialog,
    applyFiltersFromDialog,
    splitFilterValue,
  };
}
