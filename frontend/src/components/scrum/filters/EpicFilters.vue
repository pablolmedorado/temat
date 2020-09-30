<template>
  <v-container fluid class="py-0">
    <v-row>
      <v-col cols="6" md="3">
        <v-text-field
          :value="filters.search"
          label="Buscar"
          prepend-icon="mdi-magnify"
          clearable
          @input="updateFilters({ search: $event })"
          @keyup.enter="$emit('apply:filters')"
        ></v-text-field>
      </v-col>
      <v-col cols="6" md="3">
        <TagAutocomplete
          :value="tagFilter"
          label="Tags"
          prepend-icon="mdi-label"
          multiple
          truncate-results
          clearable
          @input="updateFilters({ tags__name__in: $event.join(',') })"
        />
      </v-col>
      <v-col cols="6" md="3">
        <v-select
          :value="filters.finished"
          :items="finishedOptions"
          item-text="label"
          item-value="value"
          label="Finalizada"
          prepend-icon="mdi-check-bold"
          clearable
          @change="updateFilters({ finished: $event })"
        />
      </v-col>
      <v-col cols="6" md="3">
        <v-btn class="my-2" color="primary" :loading="loading" :disabled="loading" @click="$emit('apply:filters')">
          Filtrar
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import FilterMixin from "@/mixins/filter-mixin";

export default {
  name: "EpicFilters",
  mixins: [FilterMixin],
  data() {
    return {
      finishedOptions: [
        { label: "Sí", value: true },
        { label: "No", value: false }
      ]
    };
  },
  computed: {
    tagFilter() {
      return this.splitFilterValue("tags__name__in");
    }
  }
};
</script>
