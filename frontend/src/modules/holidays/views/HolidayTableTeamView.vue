<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6"> Vacaciones del equipo ({{ year }}) </v-toolbar-title>
            <v-spacer />
            <v-tooltip v-if="canManage" bottom>
              <template #activator="{ on }">
                <v-btn icon v-on="on" @click="$refs.holidayManagementDialog.open()">
                  <v-icon>mdi-table-check</v-icon>
                </v-btn>
              </template>
              <span>Gestionar</span>
            </v-tooltip>
            <v-menu bottom left offset-y>
              <template #activator="{ on: menu }">
                <v-tooltip bottom>
                  <template #activator="{ on: tooltip }">
                    <v-btn icon :disabled="isLoading" v-on="{ ...tooltip, ...menu }">
                      <v-icon>mdi-calendar-range</v-icon>
                    </v-btn>
                  </template>
                  <span>Año</span>
                </v-tooltip>
              </template>
              <v-list>
                <v-list-item v-for="item in yearOptions" :key="item" @click="year = item">
                  <v-list-item-title>{{ item }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
            <v-tooltip bottom>
              <template #activator="{ attrs, on }">
                <v-btn icon :disabled="isTaskLoading('fetch-holidays')" v-bind="attrs" v-on="on" @click="fetchHolidays">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </template>
              <span>Refrescar</span>
            </v-tooltip>
          </v-toolbar>
          <v-card-text>
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
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <HolidayManagementDialog ref="holidayManagementDialog" @change:holiday="onHolidayChange" />
  </v-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { DateTime, Interval } from "luxon";
import { countBy, get, pick, set } from "lodash";

import Holiday from "@/modules/holidays/models/holiday";

import HolidayService from "@/modules/holidays/services/holiday-service";

import HolidayManagementDialog from "@/modules/holidays/components/dialogs/HolidayManagementDialog";
import HolidayTableCell from "@/modules/holidays/components/HolidayTableCell";

import useLoading from "@/composables/useLoading";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "HolidayTableTeamView",
  metaInfo() {
    return {
      title: `Vacaciones ${this.year}`,
    };
  },
  components: {
    HolidayManagementDialog,
    HolidayTableCell,
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
      year: DateTime.local().year,
      holidays: [],
    };
  },
  computed: {
    ...mapState(["locale"]),
    ...mapGetters(["yearOptions"]),
    ...mapGetters("users", ["workerUsers"]),
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
    canManage() {
      return userHasPermission(Holiday.CHANGE_PERMISSION);
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
