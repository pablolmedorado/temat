<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" :max-width="maxWidth" persistent scrollable>
    <v-card :loading="isFormLoading">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">
          <slot name="header">Creación múltiple</slot>
        </v-toolbar-title>
      </v-toolbar>
      <v-card-text class="pa-0">
        <v-stepper v-model="step" class="elevation-0">
          <v-stepper-header>
            <v-stepper-step :complete="step > 1" step="1">Selección de fechas</v-stepper-step>
            <v-divider />
            <v-stepper-step step="2">Asignación</v-stepper-step>
          </v-stepper-header>

          <v-stepper-items>
            <v-stepper-content step="1">
              <v-date-picker
                v-model="datesToCreate"
                :locale="locale"
                first-day-of-week="1"
                color="primary"
                full-width
                multiple
              />
            </v-stepper-content>
            <v-stepper-content step="2">
              <component
                :is="formComponent"
                v-if="Boolean(itemsToCreate.length)"
                ref="itemsForm"
                :source-items="itemsToCreate"
                @changed:items="itemsHaveChanged = $event"
                @change:loading="isFormLoading = $event"
              />
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-btn color="warning" text :disabled="isFormLoading" @click="reset">Restablecer</v-btn>
        <v-spacer />
        <v-btn text :disabled="isFormLoading" @click="close">Cancelar</v-btn>
        <v-btn text :disabled="!datesToCreate.length" :loading="isFormLoading" @click="next">
          {{ nextText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { computed, ref, toRefs } from "@vue/composition-api";

import { useMainStore } from "@/stores/main";

import { useDialog, dialogProps } from "@/composables/dialog";

export default {
  name: "StepperBulkFormDialog",
  inheritAttrs: false,
  props: {
    ...dialogProps,
    formComponent: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit, refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { showDialog, open, close: _close } = useDialog();

    // State
    const step = ref(1);
    const datesToCreate = ref([]);
    const itemsToCreate = ref([]);
    const itemsHaveChanged = ref(false);
    const isFormLoading = ref(false);

    // Computed
    const { locale } = toRefs(store);
    const nextText = computed(() => {
      return step.value < 2 ? "Siguiente" : "Guardar";
    });

    // Methods
    function reset() {
      datesToCreate.value = [];
      itemsToCreate.value = [];
      step.value = 1;
    }
    function close() {
      reset();
      _close();
    }
    function step2() {
      itemsToCreate.value = datesToCreate.value.map((date) => {
        return { date, user: null };
      });
      step.value = 2;
    }
    async function submit() {
      const newItems = await refs.itemsForm.submit();
      if (newItems) {
        emit("submit", newItems);
        close();
      }
    }
    function next() {
      step.value < 2 ? step2() : submit();
    }

    return {
      // State
      showDialog,
      step,
      datesToCreate,
      itemsToCreate,
      itemsHaveChanged,
      isFormLoading,
      // Computed
      locale,
      nextText,
      // Methods
      open,
      close,
      next,
      step2,
      reset,
      submit,
    };
  },
};
</script>
