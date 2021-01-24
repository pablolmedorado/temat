<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" max-width="500" @click:outside="close" @keydown.esc="close">
    <v-card v-if="item">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Voluntarios ({{ item.date }}) </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-chip-group column>
          <UserPill v-for="(volunteer, index) in item.volunteers" :key="`volunteer-${index}`" :user="volunteer" />
        </v-chip-group>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" text @click="close">
          Volver
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "VoluteersDialog",
  mixins: [DialogMixin],
  data() {
    return {
      item: null,
    };
  },
  methods: {
    open(item) {
      this.item = item;
      this.showDialog = true;
    },
    close() {
      this.item = null;
      this.showDialog = false;
    },
  },
};
</script>
