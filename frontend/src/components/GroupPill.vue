<template>
  <v-chip v-if="localGroup" v-bind="$attrs" pill v-on="$listeners">
    <v-avatar left color="teal">
      <v-icon color="white">mdi-account-group</v-icon>
    </v-avatar>
    {{ localGroup.name }}
  </v-chip>
</template>

<script>
import { ref, watch } from "@vue/composition-api";

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
  setup(props) {
    // Store
    const userStore = useUserStore();

    // State
    const localGroup = ref(null);

    // Watchers
    watch(
      () => props.group,
      (newValue) => {
        localGroup.value = typeof newValue == "number" ? userStore.groupMap[newValue] : newValue;
      },
      { deep: true, immediate: true }
    );

    return {
      // State
      localGroup,
    };
  },
};
</script>
