<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" :width="width" max-width="500" persistent scrollable>
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Selección de columnas </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-row>
          <v-col>
            <v-list flat>
              <v-list-item-group v-model="selectedHeaders" multiple>
                <v-list-item
                  v-for="header in availableHeaders"
                  :key="header.value"
                  :disabled="header.fixed"
                  :value="header.value"
                >
                  <template #default="{ active }">
                    <v-list-item-content>
                      <v-list-item-title>{{ header.text }}</v-list-item-title>
                    </v-list-item-content>
                    <v-list-item-action>
                      <v-checkbox :input-value="active" :true-value="header.value" :disabled="header.fixed" />
                    </v-list-item-action>
                  </template>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-col>
        </v-row>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-btn color="warning" text @click="resetHeaders">Restablecer</v-btn>
        <v-spacer />
        <v-btn text @click="close">Cancelar</v-btn>
        <v-btn text @click="applyChanges">Aplicar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "TableHeadersConfigDialog",
  mixins: [DialogMixin],
  props: {
    availableHeaders: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      selectedHeaders: this.headers.map((header) => header.value),
    };
  },
  computed: {
    defaultHeaders() {
      return this.availableHeaders.filter((header) => header.default || header.fixed).map((header) => header.value);
    },
  },
  methods: {
    applyChanges() {
      const selectedHeaders = this.availableHeaders.filter((header) => {
        return this.selectedHeaders.includes(header.value);
      });
      this.$emit("update:headers", selectedHeaders);
      this.close();
    },
    resetHeaders() {
      this.selectedHeaders = this.defaultHeaders;
    },
  },
};
</script>
