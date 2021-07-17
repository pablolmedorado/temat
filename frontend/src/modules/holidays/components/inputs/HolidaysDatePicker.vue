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
import { mapGetters, mapState } from "vuex";
import { DateTime, Interval } from "luxon";
import { defaultTo, property } from "lodash";

import HolidayService from "@/modules/holidays/services/holiday-service";
import EventService from "@/modules/calendar/services/event-service";

import useLoading from "@/composables/useLoading";

const currentDate = DateTime.local();

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
  setup() {
    const { isLoading, addTask, removeTask } = useLoading();
    return {
      isLoading,
      addTask,
      removeTask,
    };
  },
  data() {
    return {
      pickerDate: currentDate.toFormat("yyyy-MM"),
      usedDates: [],
      importantDates: [],
      summary: {},
    };
  },
  computed: {
    ...mapState(["locale", "loggedUser"]),
    ...mapGetters("users", ["workerUsers"]),
    pickerInterval() {
      const date = DateTime.fromObject({ year: this.year });
      const startDate = date.startOf("year");
      const endDate = date.endOf("year").plus({ year: 1 });
      return Interval.fromDateTimes(startDate, endDate);
    },
  },
  watch: {
    year(newValue) {
      this.$emit("input", this.multiple || this.range ? [] : null);
      this.pickerDate =
        newValue === currentDate.year
          ? currentDate.toFormat("yyyy-MM")
          : DateTime.fromObject({ year: newValue }).toFormat("yyyy-MM");
      this.getSummary();
      this.getImportantDatesByYear(newValue);
      if (this.disableUserHolidays) {
        this.getUsedDates();
      }
    },
    range(newValue) {
      if (newValue) {
        this.$emit("input", this.value ? [this.value] : []);
      } else {
        this.$emit("input", this.value ? this.value[0] : null);
      }
    },
  },
  created() {
    this.getImportantDatesByYear(this.year);
  },
  activated() {
    this.getSummary();
    if (this.disableUserHolidays) {
      this.getUsedDates();
    }
  },
  methods: {
    async getImportantDatesByYear(year) {
      this.addTask("fetch-important-dates");
      try {
        const response = await EventService.myImportantDatesByYear(year);
        this.importantDates = response.data;
      } finally {
        this.removeTask("fetch-important-dates");
      }
    },
    async getSummary() {
      this.addTask("fetch-summary");
      try {
        const response = await HolidayService.summary({ allowance_date__year: this.year });
        this.summary = Object.fromEntries(response.data.map((item) => [item.date, item.users]));
      } finally {
        this.removeTask("fetch-summary");
      }
    },
    async getUsedDates() {
      this.addTask("fetch-used-dates");
      try {
        const response = await HolidayService.list({
          user_id: this.loggedUser.id,
          planned_date__gte: this.pickerInterval.start.toISODate(),
          planned_date__lte: this.pickerInterval.end.toISODate(),
          fields: "planned_date",
        });
        this.usedDates = response.data.map(property("planned_date"));
      } finally {
        this.removeTask("fetch-used-dates");
      }
    },
    allowedDates(date) {
      return this.disableUserHolidays ? !this.usedDates.includes(date) : true;
    },
    summaryDateColour(date) {
      const userRatio = (defaultTo(this.summary[date], 0) * 100) / this.workerUsers.length;
      if (userRatio < 20) {
        return "green";
      }
      if (userRatio < 50) {
        return "orange";
      }
      return "red";
    },
    pickerEvents(date) {
      const events = [];
      if (this.importantDates.includes(date)) {
        events.push("black");
      }
      if (this.summary[date]) {
        events.push(this.summaryDateColour(date));
      }
      return events;
    },
    clear() {
      if (this.multiple || this.range) {
        this.$emit("input", []);
      } else {
        this.$emit("input", null);
      }
    },
  },
};
</script>
