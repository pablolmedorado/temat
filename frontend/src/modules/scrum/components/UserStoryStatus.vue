<template>
  <v-stepper :value="userStory.status" flat>
    <v-stepper-header>
      <template v-for="(status, index) in userStoryStatus">
        <v-stepper-step
          :key="status.value"
          :step="status.value"
          :complete="userStory.status > status.value"
          :color="userStory.status > status.value ? 'green' : 'primary'"
        >
          {{ status.label }}
        </v-stepper-step>
        <v-divider v-if="index < userStoryStatus.length - 1" :key="status.label" />
      </template>
    </v-stepper-header>
  </v-stepper>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "UserStoryStatus",
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapState("scrum", ["userStoryStatus"]),
  },
};
</script>
