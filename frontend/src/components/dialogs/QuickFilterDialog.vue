<template>
  <v-dialog v-model="showDialog" max-width="500" @click:outside="close" @keydown.esc="close">
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Guardar filtro rápido </v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-row>
          <v-col>
            <v-combobox
              v-model="newQuickFilter"
              :items="quickFilters"
              item-text="label"
              label="Nombre*"
              :error-messages="getErrorMsgs(v$.newQuickFilter)"
              @change="v$.newQuickFilter.$touch()"
              @blur="v$.newQuickFilter.$touch()"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-alert type="warning" border="left" text outlined>
              Los filtros rápidos se almacenan en el local storage del navegador y se pierden al limpiar los datos de
              navegación.
            </v-alert>
          </v-col>
        </v-row>
        <small>* indica campo obligatorio</small>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn text @click.stop="close"> Volver </v-btn>
        <v-btn text :disabled="v$.$invalid" @click="addQuickFilter">
          {{ isObject(newQuickFilter) ? "Actualizar" : "Guardar" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { nextTick, ref, watch } from "@vue/composition-api";
import { required } from "@vuelidate/validators";
import { isObject } from "lodash-es";

import { useDialog, dialogProps } from "@/composables/dialog";
import { useValidations } from "@/composables/validations";

export default {
  name: "QuickFilterDialog",
  props: {
    ...dialogProps,
    quickFilters: {
      type: Array,
      required: true,
    },
  },
  validations() {
    return {
      newQuickFilter: { required },
    };
  },
  setup(props, { emit }) {
    // Composables
    const { v$, getErrorMsgs } = useValidations();
    const { showDialog, open, close } = useDialog();

    // State
    const newQuickFilter = ref(undefined);

    // Watchers
    watch(showDialog, () => {
      newQuickFilter.value = undefined;
      v$.value.$reset();
    });

    // Methods
    function addQuickFilter() {
      nextTick(() => {
        emit("add:quick-filter", newQuickFilter.value);
        close();
      });
    }

    return {
      v$,
      // State
      showDialog,
      newQuickFilter,
      // Methods
      open,
      close,
      isObject,
      getErrorMsgs,
      addQuickFilter,
    };
  },
};
</script>
