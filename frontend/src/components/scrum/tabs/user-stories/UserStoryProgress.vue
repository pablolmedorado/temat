<template>
  <v-row>
    <template v-if="userStory.id">
      <v-col v-if="!items.length && !loading">
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
            <v-container>
              <UserStoryProgressChart :chart-data="items" :from="userStory.start_date" :to="userStory.end_date" />
            </v-container>
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
import { mapGetters } from "vuex";

import UserStoryService from "@/services/scrum/user-story-service";

import UserStoryProgressChart from "@/components/scrum/charts/UserStoryProgressChart";

export default {
  name: "UserStoryProgress",
  components: { UserStoryProgressChart },
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      items: [],
    };
  },
  computed: {
    ...mapGetters(["loading"]),
  },
  watch: {
    "userStory.id": {
      handler(newValue) {
        if (newValue) {
          this.fetchItems();
        } else {
          this.items = [];
        }
      },
      immediate: true,
    },
  },
  methods: {
    async fetchItems() {
      const response = await UserStoryService.progressByUserStory(this.userStory.id);
      this.items = response.data.results ? response.data.results : response.data;
    },
  },
};
</script>
