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
import { mapState } from "pinia";
import { DateTime } from "luxon";
import { defaultTo } from "lodash";

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
  computed: {
    ...mapState(useUserStore, ["userMap"]),
    lastModificationUser() {
      return this.event.modification_user
        ? this.userMap[this.event.modification_user]
        : this.userMap[this.event.creation_user];
    },
    lastModificationDatetime() {
      const lastModification = defaultTo(this.event.modification_datetime, this.event.creation_datetime);
      return DateTime.fromISO(lastModification).toFormat("yyyy-MM-dd HH:mm");
    },
  },
};
</script>
