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
import { ref, toRefs } from "@vue/composition-api";
import { invoke } from "lodash-es";
import { DateTime } from "luxon";

import Holiday from "@/modules/holidays/models/holiday";

import { useMainStore } from "@/stores/main";

import HolidayManagementDialog from "@/modules/holidays/components/dialogs/HolidayManagementDialog";
import HolidayTable from "@/modules/holidays/components/HolidayTable";

import { useLoading } from "@/composables/loading";

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
  setup(props, { refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { isLoading } = useLoading({
      includedChildren: ["holidayTable"],
    });

    // State
    const year = ref(DateTime.local().year);
    const canManage = userHasPermission(Holiday.CHANGE_PERMISSION);

    // Computed
    const { yearOptions } = toRefs(store);

    // Methods
    function refresh() {
      invoke(refs, "holidayTable.fetchHolidays");
    }
    function onHolidayChange(holiday) {
      invoke(refs, "holidayTable.onHolidayChange", holiday);
    }

    return {
      // State
      year,
      canManage,
      // Computed
      isLoading,
      yearOptions,
      // Functions
      refresh,
      onHolidayChange,
    };
  },
};
</script>
