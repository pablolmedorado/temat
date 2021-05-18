<template>
  <div>
    <v-tooltip bottom>
      <template #activator="{ attrs, on }">
        <v-btn icon :disabled="disabled" v-bind="attrs" v-on="on" @click="$refs.customHeadersDialog.open()">
          <v-icon>mdi-table-eye</v-icon>
        </v-btn>
      </template>
      <span>Columnas visibles</span>
    </v-tooltip>
    <TableHeadersConfigDialog
      ref="customHeadersDialog"
      :available-headers="availableHeaders"
      :headers="headers"
      @update:headers="$emit('update:headers', $event)"
    />
  </div>
</template>

<script>
export default {
  name: "TableHeaderManager",
  props: {
    availableHeaders: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
    disabled: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
