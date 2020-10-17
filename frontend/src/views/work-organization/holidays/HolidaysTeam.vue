<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12" md="4">
        <TeamHolidayFilters ref="filterComponent" :filters.sync="filters" @apply:filters="fetchItems" />
      </v-col>
      <v-col cols="12" md="8">
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6">
              Vacaciones del equipo
            </v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon :disabled="loading" @click="fetchItems">
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-toolbar>
          <ItemTable
            ref="itemTable"
            :service="service"
            :headers="tableHeaders"
            :options.sync="tableOptions"
            :system-filters="filters"
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
              <v-chip :color="getHolidayStatusRepresentation(value).colour" dark>
                <v-icon small>{{ getHolidayStatusRepresentation(value).icon }}</v-icon>
              </v-chip>
            </template>
            <template #item.table_actions="{ item }">
              <span class="d-inline-flex">
                <v-btn
                  v-show="[null, false].includes(item.approved)"
                  :disabled="loading"
                  icon
                  @click="editHoliday(item, true)"
                >
                  <v-icon>mdi-check</v-icon>
                </v-btn>
                <v-btn
                  v-show="[null, true].includes(item.approved)"
                  :disabled="loading"
                  icon
                  @click="editHoliday(item, false)"
                >
                  <v-icon>mdi-cancel</v-icon>
                </v-btn>
                <v-btn :disabled="loading" icon @click="cancelHoliday(item)">
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
import HolidaysMixin from "@/mixins/work-organization/holidays/holidays-mixin";

import HolidayService from "@/services/work-organization/holiday-service";

import TeamHolidayFilters from "@/components/work-organization/holidays/filters/TeamHolidayFilters";

import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "HolidaysTeam",
  components: { TeamHolidayFilters },
  mixins: [HolidaysMixin],
  data() {
    return {
      service: HolidayService,
      tableOptions: {
        ...defaultTableOptions,
        sortBy: ["planned_date"],
        sortDesc: [true],
        mustSort: true,
      },
      filters: {
        planned_date__isnull: false,
      },
    };
  },
  computed: {
    tableHeaders() {
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
      return this.loggedUser.is_staff ? adminOptions : defaultOptions;
    },
  },
  methods: {
    fetchItems() {
      this.$refs.itemTable.fetchItems();
    },
    getSummary() {
      this.$refs.filterComponent.getSummary();
    },
    async editHoliday(item, approved) {
      await HolidayService.changeApprovalStatus(item.id, approved);
      this.fetchItems();
      this.showSnackbar({
        color: "success",
        message: "Día de vacaciones modificado correctamente",
      });
    },
  },
};
</script>
