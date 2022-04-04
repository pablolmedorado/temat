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
import { computed, toRefs } from "@vue/composition-api";

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
  setup(props) {
    // Store
    const mainStore = useMainStore();
    const userStore = useUserStore();

    // Computed
    const { isKonamiCodeActive } = toRefs(mainStore);
    const localUser = computed(() => (typeof props.user == "number" ? userStore.userMap[props.user] : props.user));

    return {
      // Computed
      isKonamiCodeActive,
      localUser,
    };
  },
};
</script>
