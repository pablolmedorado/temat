<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" scrollable persistent :max-width="600">
    <v-card>
      <v-card-title class="text-h6"> Detalle de vacaciones {{ type }} </v-card-title>
      <v-card-text class="pa-0">
        <v-data-table
          :headers="headers"
          :items="holidaysSummary"
          :options="options"
          :disable-pagination="true"
          :hide-default-footer="true"
          no-data-text="No hay días de vacaciones con estas características"
          item-key="allowance_date"
          multi-sort
          must-sort
        />
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="close">Volver</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { chain } from "lodash";

import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "HolidaysDetailDialog",
  mixins: [DialogMixin],
  data() {
    return {
      headers: [
        { text: "Fecha de concesión", align: "start", sortable: true, value: "allowance_date" },
        {
          text: "Fecha de caducidad",
          align: "start",
          sortable: true,
          value: "expiration_date"
        },
        { text: "Total", align: "start", sortable: true, value: "count" }
      ],
      options: {
        sortBy: ["expiration_date", "allowance_date"],
        sortDesc: [false, false],
        mustSort: true
      },
      holidays: [],
      type: null
    };
  },
  computed: {
    holidaysSummary() {
      return chain(this.holidays)
        .countBy(item => [item.allowance_date, item.expiration_date])
        .map((count, item) => {
          const dates = item.split(",");
          return { allowance_date: dates[0], expiration_date: dates[1], count };
        })
        .value();
    }
  },
  methods: {
    open({ holidays, type }) {
      this.holidays = holidays;
      this.type = type;
      this.showDialog = true;
    },
    close() {
      this.holidays = [];
      this.type = null;
      this.showDialog = false;
    }
  }
};
</script>
