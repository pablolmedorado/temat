<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" :width="width" :max-width="700" persistent scrollable>
    <v-card :loading="isLoading">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Actualización en bloque </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-row>
          <v-col>
            <AsyncAutocomplete
              v-model="sprint"
              :service="sprintService"
              search-field="name"
              search-lookup="icontains"
              label="Sprint"
              prepend-icon="mdi-run-fast"
              :disabled="isLoading"
              clearable
              return-object
              @change="confirmation = false"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field
              :value="sprint ? sprint.start_date : undefined"
              label="Fecha de inicio planificada"
              prepend-icon="mdi-calendar-start"
              disabled
            />
          </v-col>
          <v-col>
            <v-text-field
              :value="sprint ? sprint.end_date : undefined"
              label="Fecha límite"
              prepend-icon="mdi-calendar-end"
              disabled
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-checkbox v-model="confirmation" :disabled="isLoading" color="warning">
              <template #label>
                Confirmo que deseo actualizar {{ items.length }} historia/s de usuario, incluyendo sus fechas
              </template>
            </v-checkbox>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn text :disabled="isLoading" @click="close">Cancelar</v-btn>
        <v-btn text :disabled="!confirmation" :loading="isLoading" @click="updateStories">Guardar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { get } from "lodash";

import DialogMixin from "@/mixins/dialog-mixin";

import SprintService from "@/modules/scrum/services/sprint-service";
import UserStoryService from "@/modules/scrum/services/user-story-service";

import useLoading from "@/composables/useLoading";
import { isoDateToLocaleString } from "@/utils/dates";

export default {
  name: "UserStoryBulkUpdateDialog",
  filters: {
    date: isoDateToLocaleString,
  },
  mixins: [DialogMixin],
  setup() {
    const { isLoading, addTask, removeTask } = useLoading();
    return {
      isLoading,
      addTask,
      removeTask,
    };
  },
  data() {
    return {
      service: UserStoryService,
      sprintService: SprintService,
      sprint: null,
      items: [],
      confirmation: false,
    };
  },
  methods: {
    open(userStories) {
      this.items = userStories;
      this.showDialog = true;
    },
    close() {
      this.sprint = null;
      this.items = [];
      this.confirmation = false;
      this.showDialog = false;
    },
    async updateStories() {
      this.addTask("update-stories");
      try {
        const payload = this.items.map((item) => ({
          id: item.id,
          sprint: get(this.sprint, "id", null),
        }));
        const params = { id__in: this.items.map((item) => item.id).join(",") };
        await this.service.bulkUpdate(payload, params);
        this.$emit("change:user-stories");
        this.close();
      } finally {
        this.removeTask("update-stories");
      }
    },
  },
};
</script>
