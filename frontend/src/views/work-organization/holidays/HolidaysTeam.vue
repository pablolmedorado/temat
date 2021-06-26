<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4">
        <TeamHolidayFilters ref="filterComponent" :filters.sync="filters" @apply:filters="fetchItems" />
      </v-col>
      <v-col cols="12" md="8">
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6"> Vacaciones del equipo </v-toolbar-title>
            <v-spacer />
            <v-btn icon :disabled="isChildLoading('itemTable')" @click="fetchItems">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-toolbar>
          <ItemTable
            ref="itemTable"
            :service="service"
            :headers="tableHeaders"
            :options.sync="tableOptions"
            :system-filters="systemFilters"
            :filters="filters"
            :elevation="0"
            no-data-text="No hay días de vacaciones coincidentes con los filtros aplicados"
            reactive-filters
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
              <span class="d-inline-flex">
                <v-btn
                  v-show="[null, false].includes(item.approved)"
                  :disabled="isLoading"
                  :loading="isTaskLoading('edit-holiday-true', item.id)"
                  icon
                  @click="editHoliday(item, true)"
                >
                  <v-icon>mdi-check</v-icon>
                </v-btn>
                <v-btn
                  v-show="[null, true].includes(item.approved)"
                  :disabled="isLoading"
                  :loading="isTaskLoading('edit-holiday-false', item.id)"
                  icon
                  @click="editHoliday(item, false)"
                >
                  <v-icon>mdi-cancel</v-icon>
                </v-btn>
                <v-btn
                  :disabled="isLoading"
                  :loading="isTaskLoading('cancel-holiday', item.id)"
                  icon
                  @click="cancelHoliday(item)"
                >
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </span>
            </template>
          </ItemTable>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { computed, ref } from "@vue/composition-api";
import { DateTime } from "luxon";

import Holiday from "@/models/work-organization/holiday";

import HolidayService from "@/services/work-organization/holiday-service";

import TeamHolidayFilters from "@/components/work-organization/holidays/filters/TeamHolidayFilters";

import useHolidays from "@/composables/useHolidays";
import useLoading from "@/composables/useLoading";
import { defaultTableOptions } from "@/utils/constants";
import { userHasPermission } from "@/utils/permissions";

const currentDate = DateTime.local();

export default {
  name: "HolidaysTeam",
  metaInfo: {
    title: "Vacaciones equipo",
  },
  components: { TeamHolidayFilters },
  setup(props, { refs }) {
    // General
    const { isLoading, isChildLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemTable"],
    });

    // Table management
    const tableOptions = ref({
      ...defaultTableOptions,
      sortBy: ["planned_date"],
      sortDesc: [false],
      multiSort: true,
    });
    const tableHeaders = computed(() => {
      const defaultOptions = [
        { text: "Fecha", align: "start", sortable: true, value: "planned_date" },
        {
          text: "Usuario",
          align: "start",
          sortable: true,
          value: "user",
          sortingField: "user__acronym",
        },
        {
          text: "Estado",
          align: "start",
          sortable: true,
          value: "approved",
        },
      ];
      const adminOptions = [
        ...defaultOptions,
        { text: "Acciones", align: "left", sortable: false, value: "table_actions" },
      ];
      return userHasPermission(Holiday.CHANGE_PERMISSION) ? adminOptions : defaultOptions;
    });
    const filters = ref({
      allowance_date__year: currentDate.year,
    });
    const systemFilters = {
      planned_date__isnull: false,
    };
    function fetchItems() {
      refs.itemTable.fetchItems();
    }

    // Holidays management
    const { edit, cancel, getStatusInfo } = useHolidays();
    async function editHoliday(item, approved) {
      addTask(`edit-holiday-${approved}`, item.id);
      try {
        await edit(item, approved);
        fetchItems();
      } finally {
        removeTask(`edit-holiday-${approved}`, item.id);
      }
    }
    async function cancelHoliday(item) {
      addTask("cancel-holiday", item.id);
      try {
        await cancel(item);
        fetchItems();
        refs.filterComponent.$refs.dateFilter.getSummary();
      } finally {
        removeTask("cancel-holiday", item.id);
      }
    }

    return {
      // General
      isLoading,
      isChildLoading,
      isTaskLoading,
      // Table management
      tableOptions,
      tableHeaders,
      filters,
      systemFilters,
      service: HolidayService,
      fetchItems,
      // Holidays management
      editHoliday,
      cancelHoliday,
      getHolidayStatusInfo: getStatusInfo,
    };
  },
};
</script>
