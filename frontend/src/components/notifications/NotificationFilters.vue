<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col cols="12" sm="6" md="3">
        <DatePickerInput
          :value="filters.timestamp__date"
          label="Fecha"
          prepend-icon="mdi-calendar"
          clearable
          @input="updateFilters({ timestamp__date: $event })"
        />
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-select
          :value="filters.target_content_type__model"
          :items="notificationTargets"
          label="Tipo"
          prepend-icon="mdi-shape"
          clearable
          @input="updateFilters({ target_content_type__model: $event })"
        >
          <template #item="{ item }">
            <v-list-item-avatar>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-avatar>
            <v-list-item-content>
              <v-list-item-title>{{ item.text }}</v-list-item-title>
            </v-list-item-content>
          </template>
        </v-select>
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-select
          :value="filters.unread"
          :items="unreadOptions"
          label="Leída"
          prepend-icon="mdi-email-open"
          clearable
          @input="updateFilters({ unread: $event })"
        />
      </v-col>
      <v-col cols="12" sm="6" md="3">
        <v-btn class="my-2" color="primary" :loading="loading" :disabled="loading" @click="$emit('apply:filters')">
          Filtrar
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapState } from "vuex";

import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "NotificationFilters",
  mixins: [FilterMixin],
  data() {
    return {
      unreadOptions: [
        { value: false, text: "Sí" },
        { value: true, text: "No" }
      ]
    };
  },
  computed: {
    ...mapState("notifications", ["notificationTargets"])
  }
};
</script>
