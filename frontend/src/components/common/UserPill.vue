<template>
  <span>
    <v-chip v-if="localUser" v-bind="$attrs" pill v-on="$listeners">
      <UserAvatar left :user="localUser" />
      {{ `${localUser.first_name} ${localUser.last_name}` }}
    </v-chip>
    <v-skeleton-loader v-else type="chip" class="mx-auto" />
  </span>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "UserPill",
  inheritAttrs: false,
  props: {
    user: {
      type: [Object, Number],
      required: true
    }
  },
  computed: {
    ...mapGetters("users", ["usersMap"]),
    localUser() {
      return typeof this.user == "number" ? this.usersMap[this.user] : this.user;
    }
  }
};
</script>
