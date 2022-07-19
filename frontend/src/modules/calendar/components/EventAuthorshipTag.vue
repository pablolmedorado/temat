<template>
  <v-tooltip v-if="Object.keys(userMap).length" bottom>
    <template #activator="{ on }">
      <v-chip class="elevation-1" v-bind="$attrs" v-on="on">
        <v-icon left>mdi-account-edit</v-icon>
        {{ lastModificationUser.acronym }}
      </v-chip>
    </template>
    <span>
      {{ `${lastModificationUser.first_name} ${lastModificationUser.last_name}` }}&nbsp;({{ lastModificationDatetime }})
    </span>
  </v-tooltip>
</template>

<script>
import { computed, toRefs } from "@vue/composition-api";
import { defaultTo } from "lodash-es";
import { DateTime } from "luxon";

import { useUserStore } from "@/stores/users";

export default {
  name: "EventAuthorshipTag",
  inheritAttrs: false,
  props: {
    event: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    // Store
    const userStore = useUserStore();

    // Computed
    const { userMap } = toRefs(userStore);
    const lastModificationUser = computed(() => {
      return props.event.modification_user
        ? userMap.value[props.event.modification_user]
        : userMap.value[props.event.creation_user];
    });
    const lastModificationDatetime = computed(() => {
      const lastModification = defaultTo(props.event.modification_datetime, props.event.creation_datetime);
      return DateTime.fromISO(lastModification).toFormat("yyyy-MM-dd HH:mm");
    });

    return {
      userMap,
      lastModificationUser,
      lastModificationDatetime,
    };
  },
};
</script>
