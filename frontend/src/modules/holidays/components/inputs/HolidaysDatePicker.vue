<template>
  <v-date-picker
    :value="value"
    v-bind="$attrs"
    :picker-date.sync="pickerDate"
    :allowed-dates="allowedDates"
    :min="pickerInterval.start.toISODate()"
    :max="pickerInterval.end.toISODate()"
    :events="pickerEvents"
    :disabled="isLoading"
    :multiple="multiple"
    :range="range"
    :locale="locale"
    locale-first-day-of-year="4"
    first-day-of-week="1"
    color="primary"
    show-week
    show-current
    full-width
    v-on="$listeners"
  />
</template>

<script>
import { computed, onActivated, ref, toRefs, watch } from "@vue/composition-api";
import { DateTime, Interval } from "luxon";
import { defaultTo, property } from "lodash-es";

import HolidayService from "@/modules/holidays/services/holiday-service";
import EventService from "@/modules/calendar/services/event-service";

import { useMainStore } from "@/stores/main";
import { useUserStore } from "@/stores/users";

import useLoading from "@/composables/useLoading";

export default {
  name: "HolidaysDatePicker",
  inheritAttrs: false,
  props: {
    value: {
      type: [String, Array],
      default: undefined,
    },
    year: {
      type: [String, Number],
      required: true,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    range: {
      type: Boolean,
      default: false,
    },
    disableUserHolidays: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    // Store
    const mainStore = useMainStore();
    const userStore = useUserStore();

    // Composables
    const { isLoading, addTask, removeTask } = useLoading();

    // State
    const currentDate = DateTime.local();
    const pickerDate = ref(currentDate.toFormat("yyyy-MM"));
    const usedDates = ref([]);
    const importantDates = ref([]);
    const summary = ref({});

    // Computed
    const { locale } = toRefs(mainStore);
    const pickerInterval = computed(() => {
      const date = DateTime.fromObject({ year: props.year });
      const startDate = date.startOf("year");
      const endDate = date.endOf("year").plus({ year: 1 });
      return Interval.fromDateTimes(startDate, endDate);
    });

    // Watchers
    watch(
      () => props.year,
      (newValue) => {
        emit("input", props.multiple || props.range ? [] : null);
        pickerDate.value =
          newValue === currentDate.year
            ? currentDate.toFormat("yyyy-MM")
            : DateTime.fromObject({ year: newValue }).toFormat("yyyy-MM");
        getSummary();
        getImportantDatesByYear(newValue);
        if (props.disableUserHolidays) {
          getUsedDates();
        }
      }
    );
    watch(
      () => props.range,
      (newValue) => {
        if (newValue) {
          emit("input", props.value ? [props.value] : []);
        } else {
          emit("input", props.value ? props.value[0] : null);
        }
      }
    );

    // Methods
    async function getImportantDatesByYear(year) {
      addTask("fetch-important-dates");
      try {
        const response = await EventService.myImportantDatesByYear(year);
        importantDates.value = response.data;
      } finally {
        removeTask("fetch-important-dates");
      }
    }
    async function getSummary() {
      addTask("fetch-summary");
      try {
        const response = await HolidayService.summary({ allowance_date__year: props.year });
        summary.value = Object.fromEntries(response.data.map((item) => [item.date, item.users]));
      } finally {
        removeTask("fetch-summary");
      }
    }
    async function getUsedDates() {
      addTask("fetch-used-dates");
      try {
        const response = await HolidayService.list({
          user_id: mainStore.currentUser.id,
          planned_date__gte: pickerInterval.value.start.toISODate(),
          planned_date__lte: pickerInterval.value.end.toISODate(),
          fields: "planned_date",
        });
        usedDates.value = response.data.map(property("planned_date"));
      } finally {
        removeTask("fetch-used-dates");
      }
    }
    function allowedDates(date) {
      return props.disableUserHolidays ? !usedDates.value.includes(date) : true;
    }
    function summaryDateColour(date) {
      const userRatio = (defaultTo(summary.value[date], 0) * 100) / userStore.workerUsers.length;
      if (userRatio < 20) {
        return "green";
      }
      if (userRatio < 50) {
        return "orange";
      }
      return "red";
    }
    function pickerEvents(date) {
      const events = [];
      if (importantDates.value.includes(date)) {
        events.push("black");
      }
      if (summary.value[date]) {
        events.push(summaryDateColour(date));
      }
      return events;
    }
    function clear() {
      if (props.multiple || props.range) {
        emit("input", []);
      } else {
        emit("input", null);
      }
    }

    // Lifecycle hooks
    onActivated(() => {
      getSummary();
      if (props.disableUserHolidays) {
        getUsedDates();
      }
    });

    // Initialization
    getImportantDatesByYear(props.year);

    return {
      // State
      pickerDate,
      // Computed
      isLoading,
      locale,
      pickerInterval,
      // Methods
      getSummary,
      getUsedDates,
      allowedDates,
      pickerEvents,
      clear,
    };
  },
};
</script>
