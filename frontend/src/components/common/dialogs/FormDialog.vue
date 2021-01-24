<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" persistent :scrollable="scrollable" :max-width="maxWidth">
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          {{ headerText }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <component :is="formComponent" v-if="item" ref="itemForm" :source-item="item" />
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-btn color="warning" text @click="reset">Restablecer</v-btn>
        <v-spacer />
        <v-btn color="primary" text @click="cancel">Cancelar</v-btn>
        <v-btn color="primary" text :loading="loading" @click="submit">
          <slot name="submit-text">Guardar</slot>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters } from "vuex";

import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "FormDialog",
  mixins: [DialogMixin],
  props: {
    verboseName: {
      type: String,
      default: "elemento",
    },
    formComponent: {
      type: Object,
      required: true,
    },
    multiAdd: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      item: null,
    };
  },
  computed: {
    ...mapGetters(["loading"]),
    headerText() {
      const verb = this.item && this.item.id ? "Editar" : "Crear";
      return `${verb} ${this.verboseName.toLowerCase()}`;
    },
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
    reset() {
      this.$refs.itemForm.reset();
    },
    async submit() {
      const item = await this.$refs.itemForm.submit();
      if (item) {
        this.$emit("submit", item);
        if (!this.item.id && this.multiAdd) {
          this.reset();
        } else {
          this.close();
        }
      }
    },
    cancel() {
      this.$emit("cancel");
      this.close();
    },
  },
};
</script>
