<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    persistent
    :scrollable="scrollable"
    :width="width"
    :max-width="maxWidth"
  >
    <v-card :loading="isFormLoading">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          {{ headerText }}
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <component
          :is="formComponent"
          v-if="item"
          ref="itemForm"
          :source-item="item"
          @changed:item="itemHasChanged = $event"
          @change:loading="isFormLoading = $event"
        />
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-btn color="warning" text :disabled="!itemHasChanged || isFormLoading" @click="reset">Restablecer</v-btn>
        <v-spacer />
        <v-btn text :disabled="isFormLoading" @click="cancel">Cancelar</v-btn>
        <v-btn text :loading="isFormLoading" @click="submit">
          <slot name="submit-text">Guardar</slot>
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { computed, ref } from "@vue/composition-api";

import useDialog, { dialogProps } from "@/composables/useDialog";

export default {
  name: "FormDialog",
  inheritAttrs: false,
  props: {
    ...dialogProps,
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
  setup(props, { emit, refs }) {
    // Composables
    const { showDialog, open: _open, close: _close } = useDialog(props);

    // State
    const item = ref(null);
    const itemHasChanged = ref(false);
    const isFormLoading = ref(false);

    // Computed
    const headerText = computed(() => {
      const verb = item.value && item.value.id ? "Editar" : "Crear";
      return `${verb} ${props.verboseName.toLowerCase()}`;
    });

    // Methods
    function open(newItem) {
      item.value = newItem;
      _open();
    }
    function close() {
      item.value = null;
      _close();
    }
    function reset() {
      refs.itemForm.reset();
    }
    async function submit() {
      const newItem = await refs.itemForm.submit();
      if (newItem) {
        emit("submit", newItem);
        if (!item.value.id && props.multiAdd) {
          reset();
        } else {
          close();
        }
      }
    }
    function cancel() {
      if (!itemHasChanged.value || confirm("Hay cambios sin guardar, ¿estás seguro que deseas salir?")) {
        close();
      }
    }

    return {
      // State
      showDialog,
      item,
      itemHasChanged,
      isFormLoading,
      // Computed
      headerText,
      // Methods
      open,
      close,
      reset,
      submit,
      cancel,
    };
  },
};
</script>
