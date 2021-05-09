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
        form-dialog-multi-add
        @submit:form="onFormSubmit"
        @delete:item="onDeleteItem"
      >
        <template #top>
          <UserStoryProgressBar class="px-4 pb-4" :user-story="userStory" />
        </template>

        <template #item.done="{ item }">
          <v-btn icon :disabled="readOnly || loading" @click="toggleItem(item)">
            <v-icon>{{ item.done ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline" }}</v-icon>
          </v-btn>
        </template>
        <template #item.table_actions="{ item }">
          <v-btn icon :disabled="loading" @click="moveItem(item, 'top')">
            <v-icon>mdi-arrow-collapse-up</v-icon>
          </v-btn>
          <v-btn icon :disabled="loading" @click="moveItem(item, 'up')">
            <v-icon>mdi-arrow-up</v-icon>
          </v-btn>
          <v-btn icon :disabled="loading" @click="moveItem(item, 'down')">
            <v-icon>mdi-arrow-down</v-icon>
          </v-btn>
          <v-btn icon :disabled="loading" @click="moveItem(item, 'bottom')">
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
import { mapGetters, mapState } from "vuex";

import TaskService from "@/services/scrum/task-service";

import TaskForm from "@/components/scrum/forms/TaskForm";
import UserStoryProgressBar from "@/components/scrum/UserStoryProgressBar";

export default {
  name: "UserStoryTasks",
  components: { UserStoryProgressBar },
  props: {
    userStory: {
      type: Object,
      required: true,
    },
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
    ...mapGetters(["loading"]),
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
      await this.service.move(item.id, action);
      this.$refs.itemIndex.fetchTableItems();
    },
    async toggleItem(item) {
      await this.service.toggle(item.id);
      this.$refs.itemIndex.fetchTableItems();
      this.$emit("change:progress");
    },
  },
};
</script>
