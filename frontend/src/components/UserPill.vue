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
import { mapState } from "pinia";

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
  computed: {
    ...mapState(useUserStore, ["userMap"]),
    localUser() {
      return typeof this.user == "number" ? this.userMap[this.user] : this.user;
    },
  },
};
</script>
