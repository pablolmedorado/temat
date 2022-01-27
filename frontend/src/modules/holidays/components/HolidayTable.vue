<template>
  <div>
    <v-skeleton-loader v-if="isLoading || !workerUsers.length" type="table" />
    <v-simple-table
      v-else
      :height="workerUsers.length >= 10 ? '600px' : undefined"
      :fixed-header="workerUsers.length >= 10"
    >
      <thead>
        <tr>
          <th class="fixed"></th>
          <th v-for="(numOfDays, month) in datesByMonth" :key="month" :colspan="numOfDays" class="first-day">
            {{ month }}
          </th>
        </tr>
        <tr>
          <th class="fixed">Usuario</th>
          <th
            v-for="date in intervalDates"
            :key="date.ts"
            :class="{ 'day-th': true, weekend: date.weekday > 5, 'first-day': date.day === 1 }"
          >
            {{ date.day }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in workerUsers" :key="user.id">
          <td class="fixed">
            <UserPill :user="user" />
          </td>
          <HolidayTableCell
            v-for="date in intervalDates"
            :key="date.ts"
            v-bind="getCellProps(user, date)"
            @change:holiday="onHolidayChange"
          />
        </tr>
      </tbody>
    </v-simple-table>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { DateTime, Interval } from "luxon";
import { countBy, get, pick, set } from "lodash";

import HolidayService from "@/modules/holidays/services/holiday-service";

import HolidayTableCell from "@/modules/holidays/components/HolidayTableCell";

import { useMainStore } from "@/stores/main";
import { useUserStore } from "@/stores/users";

import useLoading from "@/composables/useLoading";

export default {
  name: "HolidayTable",
  components: {
    HolidayTableCell,
  },
  props: {
    year: {
      type: Number,
      required: true,
    },
  },
  setup() {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();

    return {
      isLoading,
      isTaskLoading,
      addTask,
      removeTask,
    };
  },
  data() {
    return {
      holidays: [],
    };
  },
  computed: {
    ...mapState(useMainStore, ["locale"]),
    ...mapState(useUserStore, ["workerUsers"]),
    intervalDates() {
      const yearDateTime = DateTime.fromObject({ year: this.year });
      return Interval.fromDateTimes(yearDateTime, yearDateTime.endOf("year"))
        .splitBy({ days: 1 })
        .map((d) => d.start);
    },
    datesByMonth() {
      return countBy(this.intervalDates, (date) => date.setLocale(this.locale).toLocaleString({ month: "long" }));
    },
    bodyData() {
      return this.holidays.reduce((previousValue, currentValue) => {
        const result = { ...previousValue };
        set(result, [currentValue.user, currentValue.planned_date], currentValue);
        return result;
      }, {});
    },
  },
  watch: {
    year() {
      this.fetchHolidays();
    },
  },
  created() {
    this.fetchHolidays();
  },
  methods: {
    async fetchHolidays() {
      this.addTask("fetch-holidays");
      try {
        const response = await HolidayService.list({
          planned_date__year: this.year,
          fields: "id,user,planned_date,approved",
        });
        this.holidays = response.data;
      } finally {
        this.removeTask("fetch-holidays");
      }
    },
    getCellProps(user, dateTime) {
      const date = dateTime.toISODate();
      return {
        date: date,
        holiday: get(this.bodyData, [user.id, date]),
        class: {
          weekend: dateTime.weekday > 5,
          "first-day": dateTime.day === 1,
        },
      };
    },
    onHolidayChange(holiday) {
      const oldHoliday = this.holidays.findIndex((item) => item.id === holiday.id);
      if (oldHoliday !== -1) {
        if (!holiday.planned_date) {
          this.holidays.splice(oldHoliday, 1);
        } else {
          const newHoliday = pick(holiday, ["id", "user", "planned_date", "approved"]);
          this.holidays.splice(oldHoliday, 1, newHoliday);
        }
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.v-data-table {
  &.v-data-table--fixed-header thead th {
    box-shadow: unset !important;
  }

  thead > tr > th.fixed:first-child {
    z-index: 3;
  }
  tbody > tr > td.fixed:first-child {
    z-index: 2;
  }

  tr {
    .fixed:first-child {
      position: sticky !important;
      position: -webkit-sticky !important;
      left: 0;
    }
    .day-th {
      text-align: center !important;
    }
    .weekend {
      background-color: rgba(0, 174, 199, 0.2);
    }
  }

  &.theme--light {
    thead > tr:last-child > th {
      border-bottom: thin solid rgba(0, 0, 0, 0.12) !important;
    }
    tr .fixed:first-child {
      background: #ffffff;
      border-right: thin solid rgba(0, 0, 0, 0.12);
    }
    tbody > tr:hover .fixed:first-child {
      background: #eeeeee;
    }
    tr .first-day {
      border-left: thin solid rgba(0, 0, 0, 0.12);
    }
  }
  &.theme--dark {
    thead > tr:last-child > th {
      border-bottom: thin solid rgba(255, 255, 255, 0.12) !important;
    }
    tr .fixed:first-child {
      background: #1e1e1e;
      border-right: thin solid rgba(255, 255, 255, 0.12);
    }
    tbody > tr:hover .fixed:first-child {
      background: #616161;
    }
    tr .first-day {
      border-left: thin solid rgba(255, 255, 255, 0.12);
    }
  }
}
</style>
