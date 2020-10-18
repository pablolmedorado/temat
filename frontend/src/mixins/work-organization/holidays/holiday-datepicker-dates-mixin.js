import { mapGetters } from "vuex";
import { defaultTo } from "lodash";

import HolidayService from "@/services/work-organization/holiday-service";
import EventService from "@/services/calendar/event-service";

export default {
  data() {
    return {
      importantDates: [],
      summary: {},
    };
  },
  computed: {
    ...mapGetters("users", ["usersWithCompany"]),
  },
  watch: {
    "filters.allowance_date__year": function(newYear) {
      this.getSummary();
      this.getImportantDatesByYear(newYear);
    },
  },
  created() {
    this.getImportantDatesByYear(this.filters.allowance_date__year);
  },
  activated() {
    this.getSummary();
  },
  methods: {
    async getImportantDatesByYear(year) {
      const response = await EventService.myImportantDatesByYear(year);
      this.importantDates = response.data;
    },
    async getSummary() {
      const response = await HolidayService.summary({ allowance_date__year: this.filters.allowance_date__year });
      this.summary = Object.fromEntries(response.data.map((item) => [item.date, item.users]));
    },
    summaryDateColour(date) {
      const userRatio = (defaultTo(this.summary[date], 0) * 100) / this.usersWithCompany.length;
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
  },
};
