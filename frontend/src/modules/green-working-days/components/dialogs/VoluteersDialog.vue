<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    :width="width"
    max-width="500"
    @click:outside="close"
    @keydown.esc="close"
  >
    <v-card v-if="item">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Voluntarios ({{ item.date }}) </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-chip-group column>
          <UserPill v-for="(volunteer, index) in item.volunteers" :key="`volunteer-${index}`" :user="volunteer" />
        </v-chip-group>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="close"> Volver </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref } from "@vue/composition-api";

import { useDialog, dialogProps } from "@/composables/dialog";

export default {
  name: "VoluteersDialog",
  inheritAttrs: false,
  props: dialogProps,
  setup() {
    // Composables
    const { showDialog, open: _open, close: _close } = useDialog();

    // State
    const item = ref(null);

    // Methods
    function open(newItem) {
      item.value = newItem;
      _open();
    }
    function close() {
      _close();
      item.value = null;
    }

    return {
      // State
      showDialog,
      item,
      // Methods
      open,
      close,
    };
  },
};
</script>
