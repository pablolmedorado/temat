import { computed, getCurrentInstance, onUnmounted, ref, watch } from "@vue/composition-api";
import { get } from "lodash";

const currentTasks = ref({});

export default function ({ includedChildren } = {}) {
  // Vue instance
  const { emit, refs, uid } = getCurrentInstance();

  // Computed
  const tasks = computed(() => get(currentTasks.value, [uid], []));
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
    return Boolean(get(child, "isLoading", false) || get(currentTasks.value[child._uid], "length"));
  }
  function getTaskIdentifier(taskName, itemId) {
    return itemId ? `${taskName}-${itemId}` : taskName;
  }
  function isTaskLoading(taskName, itemId) {
    return tasks.value.includes(getTaskIdentifier(taskName, itemId));
  }
  function addTask(taskName, itemId) {
    const taskIdentifier = getTaskIdentifier(taskName, itemId);
    if (!currentTasks.value[uid] || !currentTasks.value[uid].includes(taskIdentifier)) {
      const tasks = { ...currentTasks.value };
      tasks[uid] = tasks[uid] ? [...tasks[uid], taskIdentifier] : [taskIdentifier];
      currentTasks.value = tasks;
      emit(`change:loading-${taskName}`, true, itemId);
    }
  }
  function removeTask(taskName, itemId) {
    const taskIdentifier = getTaskIdentifier(taskName, itemId);
    if (currentTasks.value[uid]) {
      const index = currentTasks.value[uid].findIndex((task) => task === taskIdentifier);
      if (index !== -1) {
        const tasks = { ...currentTasks.value };
        if (tasks[uid].length > 1) {
          tasks[uid].splice(index, 1);
        } else {
          delete tasks[uid];
        }
        currentTasks.value = tasks;
        emit(`change:loading-${taskName}`, false, itemId);
      }
    }
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
  onUnmounted(() => {
    if (currentTasks.value[uid]) {
      const tasks = { ...currentTasks.value };
      delete tasks[uid];
      currentTasks.value = tasks;
    }
  });

  return {
    isLoading,
    isChildLoading,
    isTaskLoading,
    addTask,
    removeTask,
    withTask,
  };
}
