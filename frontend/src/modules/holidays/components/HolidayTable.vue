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
import { computed, ref, toRefs, watch } from "@vue/composition-api";
import { DateTime, Interval } from "luxon";
import { countBy, get, pick, set } from "lodash-es";

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
  setup(props) {
    // Store
    const mainStore = useMainStore();
    const userStore = useUserStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();

    // State
    const holidays = ref([]);

    // Computed
    const { workerUsers } = toRefs(userStore);
    const intervalDates = computed(() => {
      const yearDateTime = DateTime.fromObject({ year: props.year });
      return Interval.fromDateTimes(yearDateTime, yearDateTime.endOf("year"))
        .splitBy({ days: 1 })
        .map((d) => d.start);
    });
    const datesByMonth = computed(() => {
      return countBy(intervalDates.value, (date) => date.setLocale(mainStore.locale).toLocaleString({ month: "long" }));
    });
    const bodyData = computed(() => {
      return holidays.value.reduce((previousValue, currentValue) => {
        const result = { ...previousValue };
        set(result, [currentValue.user, currentValue.planned_date], currentValue);
        return result;
      }, {});
    });

    // Watchers
    watch(() => props.year, fetchHolidays);

    // Methods
    async function fetchHolidays() {
      addTask("fetch-holidays");
      try {
        const response = await HolidayService.list({
          planned_date__year: props.year,
          fields: "id,user,planned_date,approved",
        });
        holidays.value = response.data;
      } finally {
        removeTask("fetch-holidays");
      }
    }
    function getCellProps(user, dateTime) {
      const date = dateTime.toISODate();
      return {
        date: date,
        holiday: get(bodyData.value, [user.id, date]),
        class: {
          weekend: dateTime.weekday > 5,
          "first-day": dateTime.day === 1,
        },
      };
    }
    function onHolidayChange(holiday) {
      const oldHoliday = holidays.value.findIndex((item) => item.id === holiday.id);
      if (oldHoliday !== -1) {
        if (!holiday.planned_date) {
          holidays.value.splice(oldHoliday, 1);
        } else {
          const newHoliday = pick(holiday, ["id", "user", "planned_date", "approved"]);
          holidays.value.splice(oldHoliday, 1, newHoliday);
        }
      }
    }

    // Initialization
    fetchHolidays();

    return {
      // State
      holidays,
      // Computed
      isLoading,
      workerUsers,
      intervalDates,
      datesByMonth,
      // Methods
      isTaskLoading,
      getCellProps,
      onHolidayChange,
    };
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
