<template>
  <v-row>
    <v-col>
      <ItemIndex
        v-if="userStory.id"
        ref="itemIndex"
        :model-class="modelClass"
        local-storage-namespace="userStoryTask"
        :table-available-headers="tableHeaders"
        :table-initial-options="tableOptions"
        :table-footer-props="tableFooterProps"
        :system-filters="systemFilters"
        :form-component="formComponent"
        :default-item="defaultItem"
        :allow-add="modelClass.ADD_PERMISSION"
        :allow-change="modelClass.CHANGE_PERMISSION"
        :allow-delete="modelClass.DELETE_PERMISSION"
        :disable-row-edition="isLoading"
        form-dialog-multi-add
        @submit:form="$emit('change:progress')"
        @delete:item="$emit('change:progress')"
      >
        <template #top>
          <UserStoryProgressBar class="px-4 pb-4" :user-story="userStory" />
        </template>

        <template #item.done="{ item }">
          <v-btn
            icon
            :disabled="isLoading || !canToggle"
            :loading="isTaskLoading('toggle-item', item.id)"
            @click="toggleItem(item)"
          >
            <v-icon>{{ item.done ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline" }}</v-icon>
          </v-btn>
        </template>
        <template #item.table_actions="{ item }">
          <v-btn
            icon
            :disabled="isLoading"
            :loading="isTaskLoading('move-item-top', item.id)"
            @click="moveItem(item, 'top')"
          >
            <v-icon>mdi-arrow-collapse-up</v-icon>
          </v-btn>
          <v-btn
            icon
            :disabled="isLoading"
            :loading="isTaskLoading('move-item-up', item.id)"
            @click="moveItem(item, 'up')"
          >
            <v-icon>mdi-arrow-up</v-icon>
          </v-btn>
          <v-btn
            icon
            :disabled="isLoading"
            :loading="isTaskLoading('move-item-down', item.id)"
            @click="moveItem(item, 'down')"
          >
            <v-icon>mdi-arrow-down</v-icon>
          </v-btn>
          <v-btn
            icon
            :disabled="isLoading"
            :loading="isTaskLoading('move-item-bottom', item.id)"
            @click="moveItem(item, 'bottom')"
          >
            <v-icon>mdi-arrow-collapse-down</v-icon>
          </v-btn>
        </template>
      </ItemIndex>
      <v-alert v-else type="info" text outlined border="left">
        Aún no ha creado la historia de usuario. Para poder añadir datos de tareas, guarde los cambios primero.
      </v-alert>
    </v-col>
  </v-row>
</template>

<script>
import { computed, onMounted, watch } from "@vue/composition-api";
import { invoke } from "lodash-es";

import Task from "@/modules/scrum/models/task";

import { useMainStore } from "@/stores/main";

import TaskForm from "@/modules/scrum/components/forms/TaskForm";
import UserStoryProgressBar from "@/modules/scrum/components/UserStoryProgressBar";

import { useLoading } from "@/composables/loading";

import { userHasPermission, userHasAnyPermission } from "@/utils/permissions";

import { getServiceByBasename } from "@/services";

export default {
  name: "UserStoryTasks",
  components: { UserStoryProgressBar },
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit, refs }) {
    // Store
    const mainStore = useMainStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });

    // State
    const modelClass = Task;
    const service = getServiceByBasename(modelClass.serviceBasename);
    const defaultTableHeaders = [
      {
        text: "Orden",
        align: "start",
        sortable: true,
        value: "order",
        fixed: true,
      },
      {
        text: "Nombre",
        align: "start",
        sortable: true,
        value: "name",
        fixed: true,
      },
      { text: "Peso", align: "start", sortable: true, value: "weight", fixed: true },
      { text: "Terminada", align: "start", sortable: true, value: "done", fixed: true },
    ];
    const adminTableHeaders = [
      ...defaultTableHeaders,
      {
        text: "Acciones",
        align: "start",
        sortable: false,
        value: "table_actions",
        fields: ["user_story"],
        fixed: true,
      },
    ];
    const tableOptions = {
      itemsPerPage: -1,
      sortBy: ["order"],
      sortDesc: [false],
      mustSort: true,
    };
    const tableFooterProps = {
      itemsPerPageOptions: [10, 25, 50, -1],
    };
    const formComponent = TaskForm;

    // Computed
    const systemFilters = computed(() => ({ user_story_id: props.userStory.id }));
    const defaultItem = computed(() => ({
      ...modelClass.getDefaults(),
      user_story: props.userStory.id,
    }));
    const tableHeaders = computed(() => {
      return userHasAnyPermission([modelClass.CHANGE_PERMISSION, modelClass.DELETE_PERMISSION])
        ? adminTableHeaders
        : defaultTableHeaders;
    });
    const canToggle = computed(() => {
      return (
        mainStore.currentUser.id === props.userStory.development_user || userHasPermission(modelClass.CHANGE_PERMISSION)
      );
    });

    // Watchers
    watch(
      () => props.userStory.id,
      () => invoke(refs, "itemIndex.fetchTableItems")
    );

    // Methods
    async function moveItem(item, action) {
      addTask(`move-item-${action}`, item.id);
      try {
        await service.move(item.id, action);
        refs.itemIndex.fetchTableItems();
      } finally {
        removeTask(`move-item-${action}`, item.id);
      }
    }
    async function toggleItem(item) {
      addTask("toggle-item", item.id);
      try {
        await service.toggle(item.id);
        refs.itemIndex.fetchTableItems();
        emit("change:progress");
      } finally {
        removeTask("toggle-item", item.id);
      }
    }

    // Lifecycle hooks
    onMounted(() => invoke(refs, "itemIndex.fetchTableItems"));

    return {
      // State
      modelClass,
      service,
      tableOptions,
      tableFooterProps,
      formComponent,
      // Computed
      isLoading,
      systemFilters,
      defaultItem,
      tableHeaders,
      canToggle,
      // Methods
      isTaskLoading,
      moveItem,
      toggleItem,
    };
  },
};
</script>
