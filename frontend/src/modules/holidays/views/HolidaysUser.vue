<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4">
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6"> Solicitud </v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-select v-model="year" :items="yearOptions" label="Año" prepend-icon="mdi-calendar-range" />
            <v-row>
              <v-col class="text-center">
                <template v-if="isTaskLoading('fetch-items')">
                  <v-skeleton-loader type="chip" class="ma-2 skeleton-chip" />
                  <v-skeleton-loader type="chip" class="ma-2 skeleton-chip" />
                </template>
                <template v-else>
                  <v-chip
                    class="ma-2"
                    color="green"
                    text-color="white"
                    @click.stop="$refs.holidaysDetailDialog.open({ holidays: pendingHolidays, type: 'disponibles' })"
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
                    @click.stop="$refs.holidaysDetailDialog.open({ holidays: expiredHolidays, type: 'caducadas' })"
                  >
                    <v-avatar left class="orange darken-4">
                      {{ expiredHolidays.length }}
                    </v-avatar>
                    Caducados
                    <v-avatar right>
                      <v-icon>mdi-calendar-remove</v-icon>
                    </v-avatar>
                  </v-chip>
                </template>
              </v-col>
              <HolidaysDetailDialog ref="holidaysDetailDialog" />
            </v-row>
            <v-row>
              <v-col>
                <HolidaysDatePicker
                  ref="holidaysDatePicker"
                  v-model="datesToRequest"
                  :year="year"
                  multiple
                  disable-user-holidays
                />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-btn icon @click.stop="showHelpDialog = true">
              <v-icon>mdi-help-circle</v-icon>
            </v-btn>
            <HolidaysHelpDialog v-model="showHelpDialog" />
            <v-spacer />
            <v-btn
              color="primary"
              :disabled="!datesToRequest.length"
              :loading="isTaskLoading('request-holidays')"
              @click="requestHolidays"
            >
              Solicitar ({{ datesToRequest.length }})
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
      <v-col cols="12" md="8">
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6"> Mis vacaciones </v-toolbar-title>
            <v-spacer />
            <v-btn icon :disabled="isTaskLoading('fetch-items')" @click="fetchItems()">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-toolbar>
          <v-data-table
            :headers="tableHeaders"
            :items="plannedHolidays"
            :options="tableOptions"
            :loading="isTaskLoading('fetch-items')"
            no-data-text="No hay días de vacaciones coincidentes con los filtros aplicados"
            disable-pagination
            hide-default-footer
            must-sort
          >
            <template #item.planned_date="{ value }">
              <DateRouterLink :date="value" />
            </template>
            <template #item.user="{ value }">
              <UserPill :user="value" />
            </template>
            <template #item.approved="{ value }">
              <v-chip :color="getHolidayStatusInfo(value).colour" dark>
                <v-icon small>{{ getHolidayStatusInfo(value).icon }}</v-icon>
              </v-chip>
            </template>
            <template #item.table_actions="{ item }">
              <template v-if="!item.approved">
                <v-btn
                  :disabled="isLoading"
                  :loading="isTaskLoading('cancel-holiday', item.id)"
                  icon
                  @click="cancelHoliday(item)"
                >
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
import { computed, ref, onActivated, watch } from "@vue/composition-api";
import { useGetters, useState } from "vuex-composition-helpers";
import { DateTime } from "luxon";

import HolidaysDatePicker from "@/modules/holidays/components/inputs/HolidaysDatePicker";
import HolidaysDetailDialog from "@/modules/holidays/components/dialogs/HolidaysDetailDialog";
import HolidaysHelpDialog from "@/modules/holidays/components/dialogs/HolidaysHelpDialog";

import HolidayService from "@/modules/holidays/services/holiday-service";

import useHolidays from "@/modules/holidays/composables/useHolidays";
import useLoading from "@/composables/useLoading";

const currentDate = DateTime.local();

export default {
  name: "HolidaysUser",
  metaInfo: {
    title: "Vacaciones usuario",
  },
  components: { HolidaysDatePicker, HolidaysDetailDialog, HolidaysHelpDialog },
  setup(props, { refs }) {
    // Vuex
    const { loggedUser } = useState(["loggedUser"]);
    const { yearOptions } = useGetters(["yearOptions"]);

    // General
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();

    // State
    const year = ref(currentDate.year);
    const showHelpDialog = ref(false);

    // Table Management
    const tableOptions = {
      sortBy: ["planned_date"],
      sortDesc: [false],
    };
    const tableHeaders = [
      {
        text: "Fecha",
        align: "start",
        sortable: true,
        value: "planned_date",
      },
      {
        text: "Estado",
        align: "start",
        sortable: true,
        value: "approved",
      },
      {
        text: "Acciones",
        align: "start",
        sortable: false,
        value: "table_actions",
      },
    ];
    const items = ref([]);
    async function fetchItems() {
      addTask("fetch-items");
      try {
        const response = await HolidayService.list({
          user_id: loggedUser.value.id,
          allowance_date__year: year.value,
          fields: "id,planned_date,approved,expiration_date,allowance_date",
        });
        items.value = response.data.results ? response.data.results : response.data;
      } finally {
        removeTask("fetch-items");
      }
    }

    // Holidays management
    const plannedHolidays = computed(() => items.value.filter((holiday) => holiday.planned_date));
    const unplannedHolidays = computed(() => items.value.filter((holiday) => !holiday.planned_date));
    const pendingHolidays = computed(() => {
      return unplannedHolidays.value.filter((holiday) => {
        return currentDate < DateTime.fromISO(holiday.expiration_date);
      });
    });
    const availableHolidays = computed(() => {
      return pendingHolidays.value.filter((holiday) => {
        return currentDate > DateTime.fromISO(holiday.allowance_date);
      });
    });
    const expiredHolidays = computed(() => {
      return unplannedHolidays.value.filter((holiday) => {
        return currentDate > DateTime.fromISO(holiday.expiration_date);
      });
    });
    const { datesToRequest, request, cancel, getStatusInfo } = useHolidays();
    async function requestHolidays() {
      addTask("request-holidays");
      try {
        await request();
        fetchItems();
        refs.holidaysDatePicker.getUsedDates();
        refs.holidaysDatePicker.getSummary();
      } finally {
        removeTask("request-holidays");
      }
    }
    async function cancelHoliday(item) {
      addTask("cancel-holiday", item.id);
      try {
        await cancel(item);
        fetchItems();
        refs.holidaysDatePicker.getUsedDates();
        refs.holidaysDatePicker.getSummary();
      } finally {
        removeTask("cancel-holiday", item.id);
      }
    }

    // Watchers
    watch(year, () => fetchItems());

    // Lifecycle hooks
    onActivated(() => {
      fetchItems();
    });

    return {
      //Vuex
      yearOptions,
      // General
      isLoading,
      isTaskLoading,
      // State
      showHelpDialog,
      year,
      // Table management
      items,
      fetchItems,
      tableOptions,
      tableHeaders,
      // Holidays management
      plannedHolidays,
      unplannedHolidays,
      pendingHolidays,
      availableHolidays,
      expiredHolidays,
      datesToRequest,
      requestHolidays,
      cancelHoliday,
      getHolidayStatusInfo: getStatusInfo,
    };
  },
};
</script>

<style scoped>
.skeleton-chip {
  display: inline-block;
}
</style>
