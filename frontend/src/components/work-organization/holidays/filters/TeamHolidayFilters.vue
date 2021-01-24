<template>
  <v-card>
    <v-toolbar flat>
      <v-toolbar-title class="text-h6">
        Filtros
      </v-toolbar-title>
    </v-toolbar>
    <v-card-text>
      <v-row>
        <v-col class="py-1">
          <v-select
            :value="filters.allowance_date__year"
            :items="yearOptions"
            label="Año"
            prepend-icon="mdi-calendar-range"
            @input="updateFilters({ allowance_date__year: $event })"
          />
        </v-col>
        <v-col class="py-1">
          <v-switch
            :value="filters.approved__isnull"
            label="Pendientes"
            inset
            @change="updateFilters({ approved__isnull: $event ? true : undefined })"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-1">
          <TeamHolidaysDateFilter
            ref="dateFilter"
            :year="filters.allowance_date__year"
            :filters="filters"
            :range="rangeSelector"
            :events="pickerEvents"
            :locale="locale"
            full-width
            @update:filters="$emit('update:filters', $event)"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-1">
          <v-switch v-model="rangeSelector" class="pl-1" label="Seleccionar rango" inset />
        </v-col>
      </v-row>
      <v-row>
        <v-col class="py-0">
          <UserAutocomplete
            class="pt-0"
            :value="userFilter"
            label="Usuarios"
            prepend-icon="mdi-account"
            multiple
            chips
            small-chips
            deletable-chips
            clearable
            @input="updateFilters({ user_id__in: $event.join(',') })"
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
      <v-btn color="warning" text @click="reset">
        Restablecer
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import DatePickerDatesMixin from "@/mixins/work-organization/holidays/holiday-datepicker-dates-mixin";
import FilterMixin from "@/mixins/filter-mixin";

import HolidaysHelpDialog from "@/components/work-organization/holidays/dialogs/HolidaysHelpDialog";
import TeamHolidaysDateFilter from "@/components/work-organization/holidays/filters/TeamHolidaysDateFilter";

export default {
  name: "TeamHolidayFilters",
  components: { HolidaysHelpDialog, TeamHolidaysDateFilter },
  mixins: [FilterMixin, DatePickerDatesMixin],
  data() {
    return {
      rangeSelector: false,
      importantDates: [],
      summary: {},
      showHelpDialog: false,
    };
  },
  computed: {
    ...mapState(["locale"]),
    ...mapGetters(["yearOptions"]),
    userFilter() {
      return this.splitFilterValue("user_id__in", true);
    },
  },
  methods: {
    reset() {
      this.$refs.dateFilter.clear();
      this.filters.user_id__in = "";
    },
  },
};
</script>
