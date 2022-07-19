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
import { ref } from "@vue/composition-api";
import { get } from "lodash-es";

import SprintService from "@/modules/scrum/services/sprint-service";
import UserStoryService from "@/modules/scrum/services/user-story-service";

import { useDialog, dialogProps } from "@/composables/dialog";
import { useLoading } from "@/composables/loading";

import { isoDateToLocaleString } from "@/utils/dates";

export default {
  name: "UserStoryBulkUpdateDialog",
  filters: {
    date: isoDateToLocaleString,
  },
  inheritAttrs: false,
  props: dialogProps,
  setup(props, { emit }) {
    // Composables
    const { isLoading, addTask, removeTask } = useLoading();
    const { showDialog, open: _open, close: _close } = useDialog();

    // State
    const sprint = ref(null);
    const items = ref([]);
    const confirmation = ref(false);

    // Methods
    function open(userStories) {
      items.value = userStories;
      return _open();
    }
    async function close() {
      await _close();
      sprint.value = null;
      items.value = [];
      confirmation.value = false;
    }
    async function updateStories() {
      addTask("update-stories");
      try {
        const payload = items.value.map((item) => ({
          id: item.id,
          sprint: get(sprint.value, "id", null),
        }));
        const params = { id__in: items.value.map((item) => item.id).join(",") };
        await UserStoryService.bulkUpdate(payload, params);
        emit("change:user-stories");
        close();
      } finally {
        removeTask("update-stories");
      }
    }

    return {
      // State
      isLoading,
      showDialog,
      sprintService: SprintService,
      sprint,
      items,
      confirmation,
      // Methods
      open,
      close,
      updateStories,
    };
  },
};
</script>
