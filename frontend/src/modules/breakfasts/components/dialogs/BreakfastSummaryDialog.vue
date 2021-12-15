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
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Resumen de tostadas </v-toolbar-title>
        <v-spacer />
        <v-tooltip v-if="isClipboardSupported" bottom>
          <template #activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on" @click="copyBreakfastsToClipboard">
              <v-icon>mdi-clipboard-text-multiple-outline</v-icon>
            </v-btn>
          </template>
          <span> Copiar al portapapeles </span>
        </v-tooltip>
      </v-toolbar>
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
        <v-btn text @click="close">Volver</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapActions } from "pinia";
import { useClipboard } from "@vueuse/core";
import { chain, property, uniqueId } from "lodash";

import DialogMixin from "@/mixins/dialog-mixin";

import { useMainStore } from "@/stores/main";

export default {
  name: "BreakfastSummaryDialog",
  mixins: [DialogMixin],
  setup() {
    const { copy: copyToClipboard, isSupported: isClipboardSupported } = useClipboard({ read: false });
    return {
      isClipboardSupported,
      copyToClipboard,
    };
  },
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
        .map((item) => chain(item).pick(["bread", "base", "ingredient1", "ingredient2"]).map(property("name")).value())
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
    clipboardSummary() {
      return this.itemSummary
        .map((item) => {
          const ingredients = [item.base, item.ingredient1, item.ingredient2].filter((item) => !!item).join(", ");
          return `${item.count} ${item.bread} con ${ingredients}`;
        })
        .join("\n");
    },
  },
  methods: {
    ...mapActions(useMainStore, ["showSnackbar"]),
    open(items) {
      this.items = items;
      this.showDialog = true;
    },
    close() {
      this.items = [];
      this.showDialog = false;
    },
    async copyBreakfastsToClipboard() {
      try {
        this.copyToClipboard(this.clipboardSummary);
        this.showSnackbar({
          color: "info",
          message: "Desayunos copiados al portapapeles",
        });
      } catch {
        this.showSnackbar({
          color: "error",
          message: "Error copiando desayunos al portapapeles",
        });
      }
    },
  },
};
</script>
