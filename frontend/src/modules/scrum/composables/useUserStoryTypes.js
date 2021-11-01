import { createNamespacedHelpers } from "vuex-composition-helpers";

const { useActions, useGetters, useState } = createNamespacedHelpers("scrum");

export default function () {
  const { userStoryTypes } = useState(["userStoryTypes"]);
  const { userStoryTypesMap } = useGetters(["userStoryTypesMap"]);
  const { getUserStoryTypes } = useActions(["getUserStoryTypes"]);

  if (!userStoryTypes.value.length) {
    getUserStoryTypes();
  }

  return {
    userStoryTypes,
    userStoryTypesMap,
    getUserStoryTypes,
  };
}
