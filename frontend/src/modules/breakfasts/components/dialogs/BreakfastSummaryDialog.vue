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
        <v-tooltip v-if="isClipboardSupported" left>
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
import { computed, ref } from "@vue/composition-api";
import { useClipboard } from "@vueuse/core";
import { countBy, map, pick, uniqueId } from "lodash-es";

import { useMainStore } from "@/stores/main";

import { useDialog, dialogProps } from "@/composables/dialog";

export default {
  name: "BreakfastSummaryDialog",
  inheritAttrs: false,
  props: dialogProps,
  setup() {
    // Store
    const store = useMainStore();

    // Composables
    const { showDialog, open: _open, close: _close } = useDialog();
    const { copy: copyToClipboard, isSupported: isClipboardSupported } = useClipboard({ read: false });

    // State
    const headers = [
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
    ];
    const options = ref({
      sortBy: ["bread", "base", "ingredient1", "ingredient2"],
      sortDesc: [false, false, false, false],
    });
    const items = ref([]);

    // Computed
    const itemSummary = computed(() => {
      const rawBreakfasts = items.value.map((breakfast) =>
        map(pick(breakfast, ["bread", "base", "ingredient1", "ingredient2"]), "name")
      );
      const breakfastsByCount = countBy(rawBreakfasts);
      return map(breakfastsByCount, (count, item) => {
        const elements = item.split(",");
        return {
          id: uniqueId("breakfast_"),
          bread: elements[0] || "",
          base: elements[1] || "",
          ingredient1: elements[2] || "",
          ingredient2: elements[3] || "",
          count,
        };
      });
    });
    const clipboardSummary = computed(() => {
      return itemSummary.value
        .map((item) => {
          const ingredients = [item.base, item.ingredient1, item.ingredient2].filter((item) => !!item).join(", ");
          return `${item.count} ${item.bread} con ${ingredients}`;
        })
        .join("\n");
    });

    // Methods
    function open(newItems) {
      items.value = newItems;
      _open();
    }
    function close() {
      _close();
      items.value = [];
    }
    function copyBreakfastsToClipboard() {
      try {
        copyToClipboard(clipboardSummary.value);
        store.showSnackbar({
          color: "info",
          message: "Desayunos copiados al portapapeles",
        });
      } catch {
        store.showSnackbar({
          color: "error",
          message: "Error copiando desayunos al portapapeles",
        });
      }
    }

    return {
      // State
      showDialog,
      headers,
      options,
      items,
      // Computed
      itemSummary,
      isClipboardSupported,
      // Methods
      open,
      close,
      copyBreakfastsToClipboard,
    };
  },
};
</script>
