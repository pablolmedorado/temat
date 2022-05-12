import { toRefs } from "@vue/composition-api";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

export function useUserStoryTypes() {
  // Store
  const userStoryStore = useUserStoryStore();

  // State
  const { userStoryTypes, userStoryTypesMap } = toRefs(userStoryStore);

  // Methods
  const getUserStoryTypes = userStoryStore.getUserStoryTypes;

  // Initialization
  if (!userStoryTypes.value.length) {
    userStoryStore.getUserStoryTypes();
  }

  return {
    // State
    userStoryTypes,
    userStoryTypesMap,
    // Methods
    getUserStoryTypes,
  };
}
