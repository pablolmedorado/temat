<template>
  <v-chip v-if="localGroup" v-bind="$attrs" pill v-on="$listeners">
    <v-avatar left color="teal">
      <v-icon color="white">mdi-account-group</v-icon>
    </v-avatar>
    {{ localGroup.name }}
  </v-chip>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "GroupPill",
  inheritAttrs: false,
  props: {
    group: {
      type: [Object, Number],
      required: true
    }
  },
  data() {
    return {
      localGroup: null
    };
  },
  computed: {
    ...mapGetters("users", ["groupsMap"])
  },
  watch: {
    group: {
      deep: true,
      immediate: true,
      handler(newVal) {
        this.localGroup = typeof newVal == "number" ? this.groupsMap[newVal] : newVal;
      }
    }
  }
};
</script>
