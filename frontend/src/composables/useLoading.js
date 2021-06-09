import { computed, getCurrentInstance, onUnmounted, watch } from "@vue/composition-api";
import { useMutations, useState } from "vuex-composition-helpers";
import { get } from "lodash";

export default function ({ includedChildren } = {}) {
  // Vue instance
  const { emit, refs, uid } = getCurrentInstance();

  // Vuex
  const { storeTasks } = useState({ storeTasks: "currentTasks" });
  const { addComponentTask, removeComponentTask, destroyComponentTasks } = useMutations([
    "addComponentTask",
    "removeComponentTask",
    "destroyComponentTasks",
  ]);

  // Computed
  const tasks = computed(() => get(storeTasks.value, [uid], []));
  const isLoading = computed(() => {
    if (tasks.value.length) {
      return true;
    }
    if (includedChildren) {
      return includedChildren.some((childRef) => isChildLoading(childRef));
    }
    return false;
  });

  // Watchers
  watch(isLoading, (newValue) => {
    emit("change:loading", newValue);
  });

  // Functions
  function isChildLoading(childRef) {
    const child = refs[childRef];
    if (!child) {
      return false;
    }
    return Boolean(get(child, "isLoading", false) || get(storeTasks.value[child._uid], "length"));
  }
  function getTaskIdentifier(taskName, itemId) {
    return itemId ? `${taskName}-${itemId}` : taskName;
  }
  function isTaskLoading(taskName, itemId) {
    return tasks.value.includes(getTaskIdentifier(taskName, itemId));
  }
  function addTask(taskName, itemId) {
    addComponentTask({ componentUid: uid, taskName: getTaskIdentifier(taskName, itemId) });
    emit(`change:loading-${taskName}`, true, itemId);
  }
  function removeTask(taskName, itemId) {
    removeComponentTask({ componentUid: uid, taskName: getTaskIdentifier(taskName, itemId) });
    emit(`change:loading-${taskName}`, false, itemId);
  }

  // HOF (Decorator)
  function withTask(fn, taskName) {
    return async function () {
      addTask(taskName);
      try {
        return await fn.apply(this, arguments);
      } finally {
        removeTask(taskName);
      }
    };
  }

  // Lifecycle hooks
  onUnmounted(() => destroyComponentTasks({ uid }));

  return {
    isLoading,
    isChildLoading,
    isTaskLoading,
    addTask,
    removeTask,
    withTask,
  };
}
