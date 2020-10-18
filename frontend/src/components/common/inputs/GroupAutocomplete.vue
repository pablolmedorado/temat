<template>
  <v-autocomplete
    v-bind="{ ...$props, ...$attrs }"
    :items="groupOptions"
    item-text="name"
    item-value="id"
    :loading="!groupOptions.length"
    v-on="$listeners"
  >
    <template v-if="multiple && truncateResults" #selection="{ item, index }">
      <v-chip v-if="index === 0" small>
        <span>{{ item.name }}</span>
      </v-chip>
      <span v-if="index === 1" class="grey--text text-caption">(+{{ value.length - 1 }} más)</span>
    </template>
    <template #item="{ item }">
      <v-list-item-avatar color="teal">
        <v-icon color="white">mdi-account-group</v-icon>
      </v-list-item-avatar>
      <v-list-item-content>
        <v-list-item-title>{{ item.name }}</v-list-item-title>
      </v-list-item-content>
    </template>
  </v-autocomplete>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "GroupAutocomplete",
  inheritAttrs: false,
  props: {
    value: {
      type: [String, Number, Array],
      default: null,
    },
    items: {
      type: Array,
      default: () => [],
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    readonly: {
      type: Boolean,
      default: false,
    },
    multiple: {
      type: Boolean,
      default: false,
    },
    truncateResults: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState("users", {
      groupOptions: "groups",
    }),
  },
};
</script>
