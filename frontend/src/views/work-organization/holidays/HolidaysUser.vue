<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title class="text-h6">Solicitud</v-card-title>
          <v-card-text>
            <v-select
              v-model="filters.allowance_date__year"
              :items="yearOptions"
              label="Año"
              prepend-icon="mdi-calendar-range"
            ></v-select>
            <v-row>
              <v-col class="text-center">
                <v-chip
                  class="ma-2"
                  color="green"
                  text-color="white"
                  @click="$refs.holidaysDetailDialog.open({ holidays: pendingHolidays, type: 'disponibles' })"
                >
                  <v-avatar left class="green darken-4">
                    {{ availableHolidays.length }}
                  </v-avatar>
                  Disponibles
                  <v-avatar right>
                    <v-icon>mdi-calendar-check</v-icon>
                  </v-avatar>
                </v-chip>
                <v-chip
                  class="ma-2"
                  color="orange"
                  text-color="white"
                  @click="$refs.holidaysDetailDialog.open({ holidays: expiredHolidays, type: 'caducadas' })"
                >
                  <v-avatar left class="orange darken-4">
                    {{ expiredHolidays.length }}
                  </v-avatar>
                  Caducados
                  <v-avatar right>
                    <v-icon>mdi-calendar-remove</v-icon>
                  </v-avatar>
                </v-chip>
              </v-col>
              <HolidaysDetailDialog ref="holidaysDetailDialog" />
            </v-row>
            <v-row>
              <v-col>
                <v-date-picker
                  v-model="datesToRequest"
                  :picker-date.sync="pickerDate"
                  :allowed-dates="allowedDates"
                  :min="pickerInterval.start.toISODate()"
                  :max="pickerInterval.end.toISODate()"
                  :events="pickerEvents"
                  :locale="locale"
                  :locale-first-day-of-year="4"
                  first-day-of-week="1"
                  color="primary"
                  show-week
                  show-current
                  full-width
                  multiple
                />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn icon @click.stop="showHelpDialog = true">
              <v-icon>mdi-help-circle</v-icon>
            </v-btn>
            <HolidaysHelpDialog v-model="showHelpDialog" />
            <v-spacer></v-spacer>
            <v-btn color="primary" :disabled="!datesToRequest.length" @click="requestHolidays">
              Solicitar ({{ datesToRequest.length }})
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="8">
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6">
              Mis vacaciones
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon :disabled="loading" @click="fetchItems">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-toolbar>
          <v-data-table
            :headers="tableHeaders"
            :items="plannedHolidays"
            :options="tableOptions"
            :loading="tableLoading"
            no-data-text="No hay días de vacaciones coincidentes con los filtros aplicados"
            disable-pagination
            hide-default-footer
            must-sort
          >
            <template #item.planned_date="{ value }">
              <DateRouterLink :date="value"></DateRouterLink>
            </template>
            <template #item.user="{ value }">
              <UserPill :user="value"></UserPill>
            </template>
            <template #item.approved="{ value }">
              <v-chip :color="getHolidayStatusRepresentation(value).colour" dark>
                <v-icon small>{{ getHolidayStatusRepresentation(value).icon }}</v-icon>
              </v-chip>
            </template>
            <template #item.table_actions="{ item }">
              <template v-if="!item.approved">
                <v-btn :disabled="loading" icon @click="cancelHoliday(item)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { DateTime, Interval } from "luxon";
import { includes, property } from "lodash";

import DatePickerDatesMixin from "@/mixins/work-organization/holidays/holiday-datepicker-dates-mixin";
import HolidaysMixin from "@/mixins/work-organization/holidays/holidays-mixin";

import HolidayService from "@/services/work-organization/holiday-service";

import HolidaysDetailDialog from "@/components/work-organization/holidays/dialogs/HolidaysDetailDialog";
import HolidaysHelpDialog from "@/components/work-organization/holidays/dialogs/HolidaysHelpDialog";

const currentDate = DateTime.local();

export default {
  name: "HolidaysUser",
  components: { HolidaysDetailDialog, HolidaysHelpDialog },
  mixins: [DatePickerDatesMixin, HolidaysMixin],
  data() {
    return {
      tableLoading: true,
      tableOptions: {
        itemsPerPage: -1,
        sortBy: ["planned_date"],
        sortDesc: [true]
      },
      tableHeaders: [
        {
          text: "Fecha",
          align: "start",
          sortable: true,
          value: "planned_date"
        },
        {
          text: "Estado",
          align: "start",
          sortable: true,
          value: "approved"
        },
        {
          text: "Acciones",
          align: "start",
          sortable: false,
          value: "table_actions"
        }
      ],
      items: [],
      datesToRequest: [],
      usedDates: [],
      pickerDate: currentDate.toFormat("yyyy-MM"),
      showHelpDialog: false
    };
  },
  computed: {
    plannedHolidays() {
      return this.items.filter(holiday => holiday.planned_date);
    },
    unplannedHolidays() {
      return this.items.filter(holiday => !holiday.planned_date);
    },
    pendingHolidays() {
      const now = DateTime.local();
      return this.unplannedHolidays.filter(holiday => {
        return now < DateTime.fromISO(holiday.expiration_date);
      });
    },
    availableHolidays() {
      const now = DateTime.local();
      return this.pendingHolidays.filter(holiday => {
        return now > DateTime.fromISO(holiday.allowance_date);
      });
    },
    expiredHolidays() {
      const now = DateTime.local();
      return this.unplannedHolidays.filter(holiday => {
        return now > DateTime.fromISO(holiday.expiration_date);
      });
    },
    pickerInterval() {
      const date = DateTime.fromObject({ year: this.filters.allowance_date__year });
      const startDate = date.startOf("year");
      const endDate = date.endOf("year").plus({ year: 1 });
      return Interval.fromDateTimes(startDate, endDate);
    }
  },
  watch: {
    "filters.allowance_date__year": function(newValue) {
      this.fetchItems();
      this.pickerDate =
        newValue === currentDate.year
          ? currentDate.toFormat("yyyy-MM")
          : DateTime.fromObject({ year: newValue }).toFormat("yyyy-MM");
      this.datesToRequest = [];
      this.getusedDates();
    }
  },
  activated() {
    this.fetchItems();
    this.getusedDates();
  },
  methods: {
    async fetchItems() {
      this.tableLoading = true;
      try {
        const response = await HolidayService.list({
          user_id: this.loggedUser.id,
          ...this.filters,
          fields: "id,planned_date,approved,expiration_date,allowance_date",
          ordering: `${this.tableOptions.sortDesc[0] ? "-" : ""}${this.tableOptions.sortBy[0]}`,
          page: this.tableOptions.page,
          page_size: this.tableOptions.itemsPerPage
        });
        this.items = this.tableOptions.itemsPerPage <= 0 ? response.data : response.data.results;
        this.itemCount = this.tableOptions.itemsPerPage <= 0 ? response.data.length : response.data.count;
      } finally {
        this.tableLoading = false;
      }
    },
    allowedDates(date) {
      return !includes(this.usedDates, date);
    },
    async getusedDates() {
      const response = await HolidayService.list({
        user_id: this.loggedUser.id,
        planned_date__gte: this.pickerInterval.start.toISODate(),
        planned_date__lte: this.pickerInterval.end.toISODate(),
        fields: "planned_date"
      });
      this.usedDates = response.data.map(property("planned_date"));
    },
    async requestHolidays() {
      if (
        this.datesToRequest.length &&
        confirm(`¿Confirmas que deseas solicitar estos ${this.datesToRequest.length} días?`)
      ) {
        await HolidayService.request(this.datesToRequest);
        this.fetchItems();
        this.getusedDates();
        this.getSummary();
        this.showSnackbar({
          color: "success",
          message: "Días de vacaciones solicitados correctamente"
        });
        this.datesToRequest = [];
      }
    }
  }
};
</script>
