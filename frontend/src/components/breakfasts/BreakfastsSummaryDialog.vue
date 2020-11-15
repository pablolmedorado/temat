<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    :max-width="maxWidth"
    scrollable
    @click:outside="close"
    @keydown.esc="close"
  >
    <v-card>
      <v-card-title class="text-h6">
        Resumen de tostadas
      </v-card-title>
      <v-card-text class="pa-0">
        <v-data-table
          :headers="headers"
          :items="itemSummary"
          :options="options"
          disable-pagination
          hide-default-footer
          multi-sort
          must-sort
        />
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" text @click="close">Volver</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { chain, property, uniqueId } from "lodash";

import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "BreakfastsSummaryDialog",
  mixins: [DialogMixin],
  data() {
    return {
      headers: [
        { text: "Pan", align: "start", sortable: true, value: "bread" },
        { text: "Base", align: "start", sortable: true, value: "base" },
        {
          text: "Primer ingrediente",
          align: "start",
          sortable: true,
          value: "ingredient1",
        },
        {
          text: "Segundo ingrediente",
          align: "start",
          sortable: true,
          value: "ingredient2",
        },
        { text: "Total", align: "start", sortable: true, value: "count" },
      ],
      options: {
        sortBy: ["bread", "base", "ingredient1", "ingredient2"],
        sortDesc: [false, false, false, false],
      },
      items: [],
    };
  },
  computed: {
    itemSummary() {
      return chain(this.items)
        .map((item) =>
          chain(item)
            .pick(["bread", "base", "ingredient1", "ingredient2"])
            .map(property("name"))
            .value()
        )
        .countBy()
        .map((count, item) => {
          const elements = item.split(",");
          return {
            id: uniqueId("breakfast_"),
            bread: elements[0] || "",
            base: elements[1] || "",
            ingredient1: elements[2] || "",
            ingredient2: elements[3] || "",
            count,
          };
        })
        .value();
    },
  },
  methods: {
    open(items) {
      this.items = items;
      this.showDialog = true;
    },
    close() {
      this.items = [];
      this.showDialog = false;
    },
  },
};
</script>
