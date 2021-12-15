import { toRefs } from "@vue/composition-api";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

export default function () {
  const userStoryStore = useUserStoryStore();
  const { userStoryTypes, userStoryTypesMap } = toRefs(userStoryStore);

  if (!userStoryTypes.value.length) {
    userStoryStore.getUserStoryTypes();
  }

  return {
    userStoryTypes,
    userStoryTypesMap,
    getUserStoryTypes: userStoryStore.getUserStoryTypes,
  };
}
