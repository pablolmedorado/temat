<template>
  <span class="d-inline-block">
    <v-chip v-if="localUser" v-bind="$attrs" pill v-on="$listeners">
      <UserAvatar left :user="localUser" />
      {{ `${localUser.first_name} ${localUser.last_name}` }}
    </v-chip>
    <v-skeleton-loader v-else type="chip" class="mx-auto" />
  </span>
</template>

<script>
import { computed } from "@vue/composition-api";

import { useUserStore } from "@/stores/users";

export default {
  name: "UserPill",
  inheritAttrs: false,
  props: {
    user: {
      type: [Object, Number],
      required: true,
    },
  },
  setup(props) {
    // Store
    const userStore = useUserStore();

    // Computed
    const localUser = computed(() => (typeof props.user == "number" ? userStore.userMap[props.user] : props.user));

    return {
      // Computed
      localUser,
    };
  },
};
</script>
