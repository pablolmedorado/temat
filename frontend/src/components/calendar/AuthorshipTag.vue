<template>
  <v-tooltip v-if="Object.keys(usersMap).length" bottom>
    <template v-slot:activator="{ on }">
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
import { mapGetters } from "vuex";
import { DateTime } from "luxon";
import { defaultTo } from "lodash";

export default {
  name: "AuthorshipTag",
  inheritAttrs: false,
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  computed: {
    ...mapGetters("users", ["usersMap"]),
    lastModificationUser() {
      return this.event.modification_user
        ? this.usersMap[this.event.modification_user]
        : this.usersMap[this.event.creation_user];
    },
    lastModificationDatetime() {
      const lastModification = defaultTo(this.event.modification_datetime, this.event.creation_datetime);
      return DateTime.fromISO(lastModification).toFormat("yyyy-MM-dd HH:mm");
    }
  }
};
</script>
