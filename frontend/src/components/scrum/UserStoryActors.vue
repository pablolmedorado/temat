<template>
  <span class="d-inline-flex">
    <UserAvatar
      v-if="userStory.development_user"
      class="mr-1"
      :size="avatarSize"
      :font-size="fontSize"
      :color="effortRolesMap.D.colour"
      :user="userStory.development_user"
      tooltip
    ></UserAvatar>
    <UserAvatar
      v-if="userStory.validation_user"
      class="mr-1"
      :size="avatarSize"
      :font-size="fontSize"
      :color="effortRolesMap.V.colour"
      :user="userStory.validation_user"
      tooltip
    ></UserAvatar>
    <UserAvatar
      v-if="userStory.support_user"
      :size="avatarSize"
      :font-size="fontSize"
      :color="effortRolesMap.S.colour"
      :user="userStory.support_user"
      tooltip
    ></UserAvatar>
  </span>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  name: "UserStoryActors",
  props: {
    userStory: {
      type: Object,
      required: true,
    },
    avatarSize: {
      type: Number,
      default: 32,
    },
    fontSize: {
      type: Number,
      default: 12,
    },
  },
  computed: {
    ...mapGetters("scrum", ["effortRolesMap"]),
  },
};
</script>
