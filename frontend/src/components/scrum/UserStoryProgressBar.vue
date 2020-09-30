<template>
  <div>
    <v-subheader class="pl-0">
      Progreso
      <v-tooltip right>
        <template v-slot:activator="{ on, attrs }">
          <v-icon class="ml-2" small v-bind="attrs" v-on="on">mdi-information</v-icon>
        </template>
        <span>
          Última actualización:
          {{ userStory.id ? isoDateTimeToLocaleString(userStory.current_progress_changed) : "Sin datos" }}
        </span>
      </v-tooltip>
    </v-subheader>
    <v-progress-linear :value="userStory.current_progress" height="25" dark>
      <strong class="progress-number">{{ userStory.current_progress }}%</strong>
    </v-progress-linear>
  </div>
</template>

<script>
import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "UserStoryProgressBar",
  props: {
    userStory: {
      type: Object,
      required: true
    }
  },
  methods: {
    isoDateTimeToLocaleString
  }
};
</script>

<style lang="scss" scoped>
.progress-number {
  text-shadow: 1px 1px #000;
}
</style>
