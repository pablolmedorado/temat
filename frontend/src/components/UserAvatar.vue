<template>
  <span>
    <template v-if="localUser">
      <v-tooltip :disabled="!tooltip" bottom>
        <template #activator="{ on }">
          <v-avatar v-bind="$attrs" :color="color" v-on="on">
            <img v-if="isKonamiCodeActive" src="@/assets/donmanue.jpg" alt="Don Manuel Ruiz de Lopera" />
            <span v-else class="white--text" :style="{ fontSize: fontSize + 'px' }">{{ localUser.acronym }}</span>
          </v-avatar>
        </template>
        <span>
          {{ `${localUser.first_name} ${localUser.last_name}` }}
        </span>
      </v-tooltip>
    </template>
    <v-skeleton-loader v-else type="avatar" class="mx-auto" />
  </span>
</template>

<script>
import { mapState } from "pinia";

import { useMainStore } from "@/stores/main";
import { useUserStore } from "@/stores/users";

export default {
  name: "UserAvatar",
  inheritAttrs: false,
  props: {
    user: {
      type: [Object, Number],
      required: true,
    },
    color: {
      type: String,
      default: "teal",
    },
    fontSize: {
      type: Number,
      default: 12,
    },
    tooltip: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    ...mapState(useMainStore, ["isKonamiCodeActive"]),
    ...mapState(useUserStore, ["userMap"]),
    localUser() {
      return typeof this.user == "number" ? this.userMap[this.user] : this.user;
    },
  },
};
</script>
