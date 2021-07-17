<template>
  <v-card>
    <v-toolbar flat>
      <v-toolbar-title class="text-h6"> Filtros </v-toolbar-title>
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
          <HolidaysDatePicker
            ref="dateFilter"
            v-model="selectedDates"
            :year="filters.allowance_date__year"
            :range="rangeSelector"
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
      <v-btn color="warning" text @click="reset"> Restablecer </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import { mapGetters } from "vuex";
import { isArray } from "lodash";

import FilterMixin from "@/mixins/filter-mixin";

import HolidaysDatePicker from "@/modules/holidays/components/inputs/HolidaysDatePicker";
import HolidaysHelpDialog from "@/modules/holidays/components/dialogs/HolidaysHelpDialog";

export default {
  name: "TeamHolidayFilters",
  components: { HolidaysDatePicker, HolidaysHelpDialog },
  mixins: [FilterMixin],
  data() {
    return {
      selectedDates: null,
      rangeSelector: false,
      showHelpDialog: false,
    };
  },
  computed: {
    ...mapGetters(["yearOptions"]),
    userFilter() {
      return this.splitFilterValue("user_id__in", true);
    },
  },
  watch: {
    selectedDates(newValue) {
      const localFilters = { ...this.filters };
      delete localFilters.planned_date__gte;
      delete localFilters.planned_date__lte;
      delete localFilters.planned_date;
      if (newValue) {
        if (isArray(newValue)) {
          if (newValue.length) {
            const sorted = [...newValue].sort();
            localFilters.planned_date__gte = sorted[0];
            localFilters.planned_date__lte = sorted[1];
          }
        } else {
          localFilters.planned_date = newValue;
        }
      }
      this.$emit("update:filters", localFilters);
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
