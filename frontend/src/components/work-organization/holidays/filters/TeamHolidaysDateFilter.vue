<template>
  <v-date-picker
    v-model="selectedDates"
    v-bind="{ ...$props, ...$attrs }"
    color="primary"
    :picker-date.sync="pickerDate"
    :min="pickerInterval.start.toISODate()"
    :max="pickerInterval.end.toISODate()"
    :locale="locale"
  />
</template>

<script>
import { mapState } from "vuex";
import { DateTime, Interval } from "luxon";
import { isArray } from "lodash";

const currentDate = DateTime.local();

export default {
  name: "TeamHolidaysDateFilter",
  inheritAttrs: false,
  props: {
    year: {
      type: [String, Number],
      required: true
    },
    filters: {
      type: Object,
      default: () => ({})
    },
    showWeek: {
      type: Boolean,
      default: true
    },
    firstDayOfWeek: {
      type: [String, Number],
      default: 1
    },
    range: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      selectedDates: null,
      pickerDate: currentDate.toFormat("yyyy-MM")
    };
  },
  computed: {
    ...mapState(["locale"]),
    pickerInterval() {
      const date = DateTime.fromObject({ year: this.year });
      const startDate = date.startOf("year");
      const endDate = date.endOf("year").plus({ year: 1 });
      return Interval.fromDateTimes(startDate, endDate);
    }
  },
  watch: {
    year(newValue) {
      this.selectedDates = null;
      this.pickerDate =
        newValue === currentDate.year
          ? currentDate.toFormat("yyyy-MM")
          : DateTime.fromObject({ year: newValue }).toFormat("yyyy-MM");
    },
    range(newValue) {
      if (newValue) {
        this.selectedDates = this.selectedDates ? [this.selectedDates] : [];
      } else {
        this.selectedDates = this.selectedDates ? this.selectedDates[0] : null;
      }
    },
    selectedDates(newValue) {
      const localFilters = { ...this.filters };
      delete localFilters.planned_date__gte;
      delete localFilters.planned_date__lte;
      delete localFilters.planned_date;
      if (newValue) {
        if (isArray(newValue)) {
          if (newValue.length) {
            const sorted = [...newValue].sort();
            localFilters.planned_date__gte = sorted[0];
            localFilters.planned_date__lte = sorted[1];
          }
        } else {
          localFilters.planned_date = newValue;
        }
      }
      this.$emit("update:filters", localFilters);
    }
  },
  methods: {
    clear() {
      this.selectedDates = this.range ? [] : null;
    }
  }
};
</script>
