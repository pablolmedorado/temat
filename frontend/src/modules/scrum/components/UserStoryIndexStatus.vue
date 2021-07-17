<template>
  <span
    v-if="riskLevelsMap[userStory.risk_level] && userStoryStatusMap[userStory.status]"
    class="d-inline-flex align-center"
  >
    <v-progress-circular
      class="mr-1"
      :rotate="-90"
      :size="32"
      :value="userStory.current_progress"
      :width="3"
      :color="riskLevelsMap[userStory.risk_level].colour"
    >
      {{ userStory.current_progress }}
    </v-progress-circular>
    <span :style="statusLabelStyle">
      {{ userStoryStatusMap[userStory.status].label }}
    </span>
    <v-tooltip v-if="userStory.validated === false" bottom>
      <template #activator="{ on, attrs }">
        <v-icon class="ml-1" color="error" v-bind="attrs" v-on="on">mdi-alert-circle-check-outline</v-icon>
      </template>
      <span> Validación rechazada </span>
    </v-tooltip>
  </span>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "UserStoryIndexStatus",
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapGetters("scrum", ["userStoryStatusMap", "riskLevelsMap"]),
    statusLabelStyle() {
      if (this.userStory.risk_level) {
        return {
          color: this.riskLevelsMap[this.userStory.risk_level].colour,
          fontWeight: "bold",
        };
      } else {
        return {};
      }
    },
  },
};
</script>

<style scoped>
::v-deep .v-progress-circular__info {
  font-size: 0.79rem;
}
</style>
