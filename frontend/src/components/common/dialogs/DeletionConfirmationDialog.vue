<template>
  <v-dialog v-model="showDialog" persistent max-width="500">
    <v-card v-if="dataToDelete">
      <v-card-title class="text-h6">
        <span v-if="isBulk">Confirmación de eliminación múltiple</span>
        <span v-else>Confirmación de eliminación</span>
      </v-card-title>
      <v-card-text>
        <p>
          Esta operación es irreversible
          <strong v-if="deleteChildItemsWarning" class="error--text underlined">
            y eliminará también todos los elementos hijos
          </strong>
        </p>
        <v-checkbox v-model="deletionConfirmation" :label="confirmationLabel"></v-checkbox>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn text @click.stop="close">Cancelar</v-btn>
        <v-btn color="error" text :disabled="!deletionConfirmation" @click="confirmDeletion">Eliminar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { isArray, isFunction } from "lodash";

import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "DeletionConfirmationDialog",
  mixins: [DialogMixin],
  props: {
    itemText: {
      type: [String, Function],
      default: "name"
    },
    deleteChildItemsWarning: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      dataToDelete: null,
      deletionConfirmation: false
    };
  },
  computed: {
    isBulk() {
      return isArray(this.dataToDelete);
    },
    confirmationLabel() {
      if (this.isBulk) {
        return `Confirmo que deseo eliminar ${this.dataToDelete.length} elementos`;
      } else {
        const representation = isFunction(this.itemText)
          ? this.itemText(this.dataToDelete)
          : this.dataToDelete[this.itemText];
        return `Confirmo que deseo eliminar el elemento '${representation}'`;
      }
    }
  },
  watch: {
    showDialog() {
      this.deletionConfirmation = false;
    }
  },
  methods: {
    open(data) {
      this.dataToDelete = data;
      this.showDialog = true;
    },
    close() {
      this.dataToDelete = null;
      this.showDialog = false;
    },
    confirmDeletion() {
      this.$emit("confirm", this.dataToDelete);
      this.close();
    }
  }
};
</script>

<style scoped>
.underlined {
  text-decoration: underline;
}
</style>
