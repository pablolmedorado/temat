<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    :width="width"
    :max-width="900"
    scrollable
    @click:outside="close"
    @keydown.esc="close"
  >
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Gestión rápida de tareas </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="pa-0">
        <ItemTable
          v-if="userStory"
          ref="itemTable"
          :service="service"
          :headers="tableHeaders"
          :options.sync="tableOptions"
          :system-filters="systemFilters"
          :elevation="0"
          no-data-text="No hay tareas"
        >
          <template #item.done="{ item }">
            <v-btn
              icon
              :disabled="isLoading || !canChange(item)"
              :loading="isTaskLoading('toggle-item', item.id)"
              @click="toggleItem(item)"
            >
              <v-icon>{{ item.done ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline" }}</v-icon>
            </v-btn>
          </template>
        </ItemTable>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="close">Volver</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { computed, ref } from "@vue/composition-api";
import { get } from "lodash-es";

import Task from "@/modules/scrum/models/task";

import { useMainStore } from "@/stores/main";

import TaskService from "@/modules/scrum/services/task-service";

import { useDialog, dialogProps } from "@/composables/dialog";
import { useLoading } from "@/composables/loading";

import { userHasPermission } from "@/utils/permissions";

export default {
  name: "TaskQuickManagementDialog",
  inheritAttrs: false,
  props: dialogProps,
  setup(props, { emit, refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemTable"],
    });
    const { showDialog, open: _open, close: _close } = useDialog();

    // State
    const tableHeaders = [
      {
        text: "Orden",
        align: "start",
        sortable: true,
        value: "order",
      },
      {
        text: "Nombre",
        align: "start",
        sortable: true,
        value: "name",
      },
      { text: "Peso", align: "start", sortable: true, value: "weight" },
      {
        text: "Terminada",
        align: "start",
        sortable: true,
        value: "done",
        fields: ["done", "user_story.development_user"],
      },
    ];
    const tableOptions = ref({
      itemsPerPage: 10,
      sortBy: ["order"],
      sortDesc: [false],
      mustSort: true,
    });
    const userStory = ref(null);
    let updateTableAfterClose = false;

    // Computed
    const systemFilters = computed(() => ({ user_story_id: get(userStory.value, "id", null) }));

    // Methods
    function canChange(item) {
      return store.currentUser.id === item.user_story.development_user || userHasPermission(Task.CHANGE_PERMISSION);
    }
    async function toggleItem(item) {
      addTask("toggle-item", item.id);
      try {
        await TaskService.toggle(item.id);
        refs.itemTable.fetchItems();
        updateTableAfterClose = true;
      } finally {
        removeTask("toggle-item", item.id);
      }
    }
    async function open(newUserStory) {
      userStory.value = newUserStory;
      await _open();
      refs.itemTable.fetchItems();
    }
    function close() {
      userStory.value = null;
      _close();
      if (updateTableAfterClose) {
        emit("change:tasks");
      }
      updateTableAfterClose = false;
    }

    return {
      // State
      isLoading,
      isTaskLoading,
      showDialog,
      service: TaskService,
      tableHeaders,
      tableOptions,
      userStory,
      // Computed
      systemFilters,
      // Methods
      open,
      close,
      canChange,
      toggleItem,
    };
  },
};
</script>
