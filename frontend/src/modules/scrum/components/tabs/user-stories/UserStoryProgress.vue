<template>
  <v-row>
    <template v-if="userStory.id">
      <v-col v-if="!items.length && !isLoading">
        <v-alert type="info" text outlined border="left">
          Aún no existen registros de avance. Se generarán al añadir tareas e interactuar con ellas.
        </v-alert>
      </v-col>
      <template v-if="items.length">
        <v-col cols="12" lg="4">
          <v-simple-table class="elevation-1">
            <template #default>
              <thead>
                <tr>
                  <th scope="col" class="text-left">Fecha</th>
                  <th scope="col" class="text-left">Avance</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in items" :key="item.id">
                  <td>{{ item.date }}</td>
                  <td>{{ item.progress }}%</td>
                </tr>
              </tbody>
            </template>
          </v-simple-table>
        </v-col>
        <v-col cols="12" lg="8">
          <v-card>
            <v-card-text>
              <UserStoryProgressChart :chart-data="items" :from="userStory.start_date" :to="userStory.end_date" />
            </v-card-text>
          </v-card>
        </v-col>
      </template>
    </template>
    <v-alert v-else type="info" text outlined border="left">
      Aún no ha creado la historia de usuario. Para poder añadir datos de progreso, guarde los cambios primero.
    </v-alert>
  </v-row>
</template>

<script>
import { ref, watch } from "@vue/composition-api";

import UserStoryService from "@/modules/scrum/services/user-story-service";

import UserStoryProgressChart from "@/modules/scrum/components/charts/UserStoryProgressChart";

import { useLoading } from "@/composables/loading";

export default {
  name: "UserStoryProgress",
  components: { UserStoryProgressChart },
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    // Composables
    const { isLoading, addTask, removeTask } = useLoading();

    // State
    const items = ref([]);

    // Watchers
    watch(
      () => props.userStory.id,
      (newValue) => {
        if (newValue) {
          fetchItems();
        } else {
          items.value = [];
        }
      },
      { immediate: true }
    );

    // Methods
    async function fetchItems() {
      addTask("fetch-items");
      try {
        const response = await UserStoryService.progressByUserStory(props.userStory.id);
        items.value = response.data.results ? response.data.results : response.data;
      } finally {
        removeTask("fetch-items");
      }
    }

    return {
      // State
      items,
      // Computed
      isLoading,
      // Methods
      fetchItems,
    };
  },
};
</script>
