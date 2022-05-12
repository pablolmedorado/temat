<template>
  <v-dialog v-model="showDialog" persistent max-width="500">
    <v-card v-if="dataToDelete">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          <span v-if="isBulk">Confirmación de eliminación múltiple</span>
          <span v-else>Confirmación de eliminación</span>
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <p>
          Esta operación es irreversible
          <strong v-if="deleteChildItemsWarning" class="error--text underlined">
            y eliminará también todos los elementos hijos
          </strong>
        </p>
        <v-checkbox v-model="deletionConfirmation" :label="confirmationLabel" />
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click.stop="close">Cancelar</v-btn>
        <v-btn color="error" text :disabled="!deletionConfirmation" @click="confirmDeletion">Eliminar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { computed, ref, watch } from "@vue/composition-api";
import { isArray, isFunction } from "lodash-es";

import { useDialog, dialogProps } from "@/composables/dialog";

export default {
  name: "DeletionConfirmationDialog",
  inheritAttrs: false,
  props: {
    ...dialogProps,
    itemText: {
      type: [String, Function],
      default: "name",
    },
    deleteChildItemsWarning: {
      type: Boolean,
      default: false,
    },
  },
  setup(props, { emit }) {
    // Composables
    const { showDialog, open: _open, close: _close } = useDialog();

    // State
    const dataToDelete = ref(null);
    const deletionConfirmation = ref(false);

    // Computed
    const isBulk = computed(() => isArray(dataToDelete.value));
    const confirmationLabel = computed(() => {
      if (isBulk.value) {
        return `Confirmo que deseo eliminar ${dataToDelete.value.length || "todos los"} elementos`;
      } else {
        const representation = isFunction(props.itemText)
          ? props.itemText(dataToDelete.value)
          : dataToDelete.value[props.itemText];
        return `Confirmo que deseo eliminar el elemento '${representation}'`;
      }
    });

    // Watchers
    watch(showDialog, () => (deletionConfirmation.value = false));

    // Methods
    function open(data) {
      dataToDelete.value = data;
      _open();
    }
    function close() {
      dataToDelete.value = null;
      _close();
    }
    function confirmDeletion() {
      emit("confirm", dataToDelete.value);
      close();
    }

    return {
      // State
      showDialog,
      dataToDelete,
      deletionConfirmation,
      // Computed
      isBulk,
      confirmationLabel,
      // Methods
      open,
      close,
      confirmDeletion,
    };
  },
};
</script>

<style scoped>
.underlined {
  text-decoration: underline;
}
</style>
