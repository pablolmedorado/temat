<template>
  <v-menu
    v-model="showMenu"
    content-class="v-dialog--scrollable"
    :min-width="400"
    :max-width="400"
    :nudge-width="200"
    bottom
    left
    offset-y
  >
    <template #activator="{ on: menu }">
      <v-tooltip bottom>
        <template #activator="{ on: tooltip }">
          <v-btn :disabled="loading" icon v-on="{ ...tooltip, ...menu }">
            <v-icon>mdi-apps</v-icon>
          </v-btn>
        </template>
        <span> Enlaces </span>
      </v-tooltip>
    </template>

    <v-card>
      <v-card-text>
        <template v-for="(links, type, index) in itemsByType">
          <v-divider v-if="index" :key="`${type}-divider`" class="my-2"></v-divider>
          <v-row :key="type" dense>
            <v-col v-for="link in links" :key="link.name" cols="4">
              <v-hover v-slot="{ hover }">
                <v-card :href="link.url" target="_blank" class="pa-2" flat ripple>
                  <div class="d-flex justify-center">
                    <v-icon x-large :color="hover ? 'secondary' : 'default'">{{ link.icon }}</v-icon>
                  </div>
                  <div class="d-flex justify-center text-center">
                    <span :class="`${hover ? 'secondary' : 'default'}--text text-truncate`">
                      {{ link.name }}
                    </span>
                  </div>
                </v-card>
              </v-hover>
            </v-col>
          </v-row>
        </template>
      </v-card-text>
    </v-card>
  </v-menu>
</template>

<script>
import { groupBy } from "lodash";

import LinkService from "@/services/common/link-service";

export default {
  name: "LinkManager",
  data() {
    return {
      showMenu: false,
      loading: false,
      items: [],
    };
  },
  computed: {
    itemsByType() {
      return groupBy(this.items, "type.order");
    },
  },
  created() {
    this.fetchItems();
  },
  methods: {
    async fetchItems() {
      try {
        this.loading = true;
        const response = await LinkService.list({ expand: "type" });
        this.items = response.data;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.v-dialog--scrollable {
  max-height: 80%;
}
</style>
