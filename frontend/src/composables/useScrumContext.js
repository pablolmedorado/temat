import { computed, provide, ref, watch } from "@vue/composition-api";

import EpicService from "@/services/scrum/epic-service";
import SprintService from "@/services/scrum/sprint-service";

export const scrumContextProps = {
  sprintId: {
    type: String,
    default: null,
  },
  epicId: {
    type: String,
    default: null,
  },
};

export default function (props) {
  const hasContext = computed(() => Boolean(props.sprintId || props.epicId));
  const context = computed(() => ({ sprint: props.sprintId, epic: props.epicId }));
  provide("context", context.value);

  const contextItem = ref(null);
  async function getContextItem() {
    let service, pk;
    if (props.sprintId) {
      service = SprintService;
      pk = props.sprintId;
    }
    if (props.epicId) {
      service = EpicService;
      pk = props.epicId;
    }
    if (service && pk) {
      const response = await service.retrieve(pk, { fields: "id,name" });
      contextItem.value = response.data;
    } else {
      contextItem.value = null;
    }
  }

  // Watchers
  watch(
    () => [props.sprintId, props.epicId],
    () => getContextItem(),
    { immediate: true, deep: true }
  );

  return {
    hasContext,
    context,
    contextItem,
  };
}
