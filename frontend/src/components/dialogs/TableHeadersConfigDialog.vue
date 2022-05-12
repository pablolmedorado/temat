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
import { computed, ref } from "@vue/composition-api";

import { useDialog, dialogProps } from "@/composables/dialog";

export default {
  name: "TableHeadersConfigDialog",
  inheritAttrs: false,
  props: {
    ...dialogProps,
    availableHeaders: {
      type: Array,
      required: true,
    },
    headers: {
      type: Array,
      required: true,
    },
  },
  setup(props, { emit }) {
    // Composables
    const { showDialog, open: _open, close: _close } = useDialog();

    // State
    const selectedHeaders = ref([]);

    // Computed
    const defaultHeaders = computed(() =>
      props.availableHeaders.filter((header) => header.default || header.fixed).map((header) => header.value)
    );

    // Methods
    function open() {
      selectedHeaders.value = props.headers.map((header) => header.value);
      _open();
    }
    function close() {
      _close();
      selectedHeaders.value = [];
    }
    function applyChanges() {
      const headers = props.availableHeaders.filter((header) => {
        return selectedHeaders.value.includes(header.value);
      });
      emit("update:headers", headers);
      close();
    }
    function resetHeaders() {
      selectedHeaders.value = defaultHeaders.value;
    }

    return {
      // State
      showDialog,
      selectedHeaders,
      // Computed
      defaultHeaders,
      // Methods
      open,
      close,
      applyChanges,
      resetHeaders,
    };
  },
};
</script>
