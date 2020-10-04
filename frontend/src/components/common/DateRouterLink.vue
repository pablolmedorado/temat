<template>
  <span class="d-inline-flex">
    {{ date | date }}
    <router-link class="ml-1" :to="{ name: 'calendar', params: { initialDate: date } }">
      <v-tooltip bottom>
        <template #activator="{ on, attrs }">
          <v-icon small v-bind="attrs" v-on="on">mdi-calendar-search</v-icon>
        </template>
        <span>
          Ver en el calendario
        </span>
      </v-tooltip>
    </router-link>
  </span>
</template>

<script>
import { isoDateToLocaleString } from "@/utils/dates";

export default {
  name: "DateRouterLink",
  filters: {
    date: isoDateToLocaleString
  },
  props: {
    date: {
      type: String,
      required: true
    }
  }
};
</script>

<style scoped>
a {
  text-decoration: none;
}
</style>
