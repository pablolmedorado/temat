import { toRefs } from "@vue/composition-api";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

export default function () {
  // Store
  const userStoryStore = useUserStoryStore();

  // State
  const { userStoryTypes, userStoryTypesMap } = toRefs(userStoryStore);

  // Lifecycle hooks
  if (!userStoryTypes.value.length) {
    userStoryStore.getUserStoryTypes();
  }

  return {
    // State
    userStoryTypes,
    userStoryTypesMap,
    // Methods
    getUserStoryTypes: userStoryStore.getUserStoryTypes,
  };
}
