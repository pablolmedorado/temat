<template>
  <span>
    <template v-if="localUser">
      <v-tooltip :disabled="!tooltip" bottom>
        <template #activator="{ on }">
          <v-avatar v-bind="$attrs" :color="color" v-on="on">
            <img v-if="konamiCodeActive" src="@/assets/donmanue.jpg" alt="Don Manuel Ruiz de Lopera" />
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
import { mapGetters, mapState } from "vuex";

export default {
  name: "UserAvatar",
  inheritAttrs: false,
  props: {
    user: {
      type: [Object, Number],
      required: true
    },
    color: {
      type: String,
      default: "teal"
    },
    fontSize: {
      type: Number,
      default: 12
    },
    tooltip: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    ...mapState(["konamiCodeActive"]),
    ...mapGetters("users", ["usersMap"]),
    localUser() {
      return typeof this.user == "number" ? this.usersMap[this.user] : this.user;
    }
  }
};
</script>
