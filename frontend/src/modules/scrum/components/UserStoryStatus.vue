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
import { toRefs } from "@vue/composition-api";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

export default {
  name: "UserStoryStatus",
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  setup() {
    // Store
    const userStoryStore = useUserStoryStore();

    // Computed
    const { userStoryStatus } = toRefs(userStoryStore);

    return {
      userStoryStatus,
    };
  },
};
</script>
