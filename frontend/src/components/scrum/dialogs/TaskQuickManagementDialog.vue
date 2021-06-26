<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    :max-width="700"
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
import { mapState } from "vuex";
import { get } from "lodash";

import Task from "@/models/scrum/task";

import DialogMixin from "@/mixins/dialog-mixin";

import TaskService from "@/services/scrum/task-service";

import useLoading from "@/composables/useLoading";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "TaskQuickManagementDialog",
  mixins: [DialogMixin],
  setup() {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemTable"],
    });
    return {
      isLoading,
      isTaskLoading,
      addTask,
      removeTask,
    };
  },
  data() {
    return {
      service: TaskService,
      tableHeaders: [
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
      ],
      tableOptions: {
        itemsPerPage: 10,
        sortBy: ["order"],
        sortDesc: [false],
        mustSort: true,
      },
      userStory: null,
      updateTableAfterTaskMgmt: false,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    systemFilters() {
      return { user_story_id: get(this.userStory, "id", null) };
    },
  },
  methods: {
    canChange(item) {
      return this.loggedUser.id === item.user_story.development_user || userHasPermission(Task.CHANGE_PERMISSION);
    },
    async toggleItem(item) {
      this.addTask("toggle-item", item.id);
      try {
        await TaskService.toggle(item.id);
        this.$refs.itemTable.fetchItems();
        this.updateTableAfterTaskMgmt = true;
      } finally {
        this.removeTask("toggle-item", item.id);
      }
    },
    open(userStory) {
      this.userStory = userStory;
      this.showDialog = true;
      this.$nextTick(() => {
        this.$refs.itemTable.fetchItems();
      });
    },
    close() {
      this.userStory = null;
      this.showDialog = false;
      if (this.updateTableAfterTaskMgmt) {
        this.$emit("updated-tasks");
      }
      this.updateTableAfterTaskMgmt = false;
    },
  },
};
</script>
