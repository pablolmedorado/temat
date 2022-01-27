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
                <v-btn icon :disabled="isLoading" v-bind="attrs" v-on="on" @click="refresh">
                  <v-icon>mdi-refresh</v-icon>
                </v-btn>
              </template>
              <span>Refrescar</span>
            </v-tooltip>
          </v-toolbar>
          <v-card-text>
            <HolidayTable ref="holidayTable" :year="year" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <HolidayManagementDialog ref="holidayManagementDialog" @change:holiday="onHolidayChange" />
  </v-container>
</template>

<script>
import { mapState } from "pinia";
import { DateTime } from "luxon";
import { invoke } from "lodash";

import Holiday from "@/modules/holidays/models/holiday";

import HolidayManagementDialog from "@/modules/holidays/components/dialogs/HolidayManagementDialog";
import HolidayTable from "@/modules/holidays/components/HolidayTable";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "HolidayTeamView",
  metaInfo() {
    return {
      title: `Vacaciones ${this.year}`,
    };
  },
  components: {
    HolidayManagementDialog,
    HolidayTable,
  },
  setup() {
    const { isLoading } = useLoading({
      includedChildren: ["holidayTable"],
    });

    return {
      isLoading,
    };
  },
  data() {
    return {
      year: DateTime.local().year,
    };
  },
  computed: {
    ...mapState(useMainStore, ["yearOptions"]),
    canManage() {
      return userHasPermission(Holiday.CHANGE_PERMISSION);
    },
  },
  methods: {
    refresh() {
      invoke(this.$refs, "holidayTable.fetchHolidays");
    },
    onHolidayChange(holiday) {
      invoke(this.$refs, "holidayTable.onHolidayChange", holiday);
    },
  },
};
</script>
