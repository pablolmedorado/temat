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
      <v-card-title class="text-h6">
        Gestión rápida de tareas.
        <template v-if="userStory">Historia: "{{ userStory.name | truncate(20) }}"</template>
      </v-card-title>
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
              :disabled="loading || (!loggedUser.is_staff && loggedUser.id !== item.user_story.development_user)"
              @click="toggleTask(item)"
            >
              <v-icon>{{ item.done ? "mdi-checkbox-marked" : "mdi-checkbox-blank-outline" }}</v-icon>
            </v-btn>
          </template>
        </ItemTable>
      </v-card-text>
      <v-divider></v-divider>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="primary" text @click="close">Volver</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { get } from "lodash";

import DialogMixin from "@/mixins/dialog-mixin";

import TaskService from "@/services/scrum/task-service";

import { truncate } from "@/filters";

export default {
  name: "TaskQuickManagementDialog",
  filters: { truncate },
  mixins: [DialogMixin],
  data() {
    return {
      service: TaskService,
      tableHeaders: [
        {
          text: "Orden",
          align: "start",
          sortable: true,
          value: "order"
        },
        {
          text: "Nombre",
          align: "start",
          sortable: true,
          value: "name"
        },
        { text: "Peso", align: "start", sortable: true, value: "weight" },
        {
          text: "Terminada",
          align: "start",
          sortable: true,
          value: "done",
          fields: ["done", "user_story.development_user"]
        }
      ],
      tableOptions: {
        itemsPerPage: 10,
        sortBy: ["order"],
        sortDesc: [false],
        mustSort: true
      },
      userStory: null,
      updateTableAfterTaskMgmt: false
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["loading"]),
    systemFilters() {
      return { user_story_id: get(this.userStory, "id", null) };
    }
  },
  methods: {
    async toggleTask(item) {
      await TaskService.toggle(item.id);
      this.$refs.itemTable.fetchItems();
      this.updateTableAfterTaskMgmt = true;
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
    }
  }
};
</script>
