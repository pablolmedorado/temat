<template>
  <v-row>
    <v-col>
      <ItemIndex
        v-if="userStory.id"
        ref="itemIndex"
        local-storage-namespace="userStoryTask"
        verbose-name="Tarea"
        verbose-name-plural="Tareas"
        :table-available-headers="tableHeaders"
        :table-initial-options="tableOptions"
        :system-filters="systemFilters"
        :service="service"
        :form-component="formComponent"
        :default-item="defaultItem"
        :read-only="readOnly"
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
            :disabled="readOnly || isLoading"
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
import { mapState } from "vuex";

import TaskService from "@/services/scrum/task-service";

import TaskForm from "@/components/scrum/forms/TaskForm";
import UserStoryProgressBar from "@/components/scrum/UserStoryProgressBar";

import useLoading from "@/composables/useLoading";

export default {
  name: "UserStoryTasks",
  components: { UserStoryProgressBar },
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  setup() {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
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
      tableOptions: {
        itemsPerPage: -1,
        sortBy: ["order"],
        sortDesc: [false],
        mustSort: true,
      },
      service: TaskService,
      formComponent: TaskForm,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    systemFilters() {
      return {
        user_story_id: this.userStory.id,
      };
    },
    defaultItem() {
      return { id: null, user_story: this.userStory.id, name: "", weight: 1, done: false };
    },
    readOnly() {
      return !this.loggedUser.is_superuser && this.loggedUser.id !== this.userStory.development_user;
    },
    tableHeaders() {
      const defaultOptions = [
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
      const adminOptions = [
        ...defaultOptions,
        {
          text: "Acciones",
          align: "start",
          sortable: false,
          value: "table_actions",
          fields: ["user_story"],
          fixed: true,
        },
      ];
      return this.loggedUser.is_superuser ? adminOptions : defaultOptions;
    },
  },
  mounted() {
    if (this.$refs.itemIndex) {
      this.$refs.itemIndex.fetchTableItems();
    }
  },
  methods: {
    onFormSubmit() {
      this.$emit("change:progress");
    },
    onDeleteItem() {
      this.$emit("change:progress");
    },
    async moveItem(item, action) {
      this.addTask(`move-item-${action}`, item.id);
      try {
        await this.service.move(item.id, action);
        this.$refs.itemIndex.fetchTableItems();
      } finally {
        this.removeTask(`move-item-${action}`, item.id);
      }
    },
    async toggleItem(item) {
      this.addTask("toggle-item", item.id);
      try {
        await this.service.toggle(item.id);
        this.$refs.itemIndex.fetchTableItems();
        this.$emit("change:progress");
      } finally {
        this.removeTask("toggle-item", item.id);
      }
    },
  },
};
</script>
