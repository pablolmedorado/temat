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
        <slot name="actions"></slot>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "BaseDialog",
  mixins: [DialogMixin],
};
</script>
