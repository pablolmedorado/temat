<template>
  <v-chip v-if="localGroup" v-bind="$attrs" pill v-on="$listeners">
    <v-avatar left color="teal">
      <v-icon color="white">mdi-account-group</v-icon>
    </v-avatar>
    {{ localGroup.name }}
  </v-chip>
</template>

<script>
import { mapState } from "pinia";

import { useUserStore } from "@/stores/users";

export default {
  name: "GroupPill",
  inheritAttrs: false,
  props: {
    group: {
      type: [Object, Number],
      required: true,
    },
  },
  data() {
    return {
      localGroup: null,
    };
  },
  computed: {
    ...mapState(useUserStore, ["groupMap"]),
  },
  watch: {
    group: {
      deep: true,
      immediate: true,
      handler(newVal) {
        this.localGroup = typeof newVal == "number" ? this.groupMap[newVal] : newVal;
      },
    },
  },
};
</script>
