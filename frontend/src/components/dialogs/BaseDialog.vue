<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    :scrollable="scrollable"
    :persistent="persistent"
    :max-width="maxWidth"
  >
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          <slot name="header"></slot>
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <slot name="body"></slot>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <slot name="actions" v-bind="{ close }"></slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import useDialog, { dialogProps } from "@/composables/useDialog";

export default {
  name: "BaseDialog",
  inheritAttrs: false,
  props: dialogProps,
  setup(props) {
    const { showDialog, open, close } = useDialog(props);
    return {
      // State
      showDialog,
      // Methods
      open,
      close,
    };
  },
};
</script>
