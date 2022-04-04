<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <v-textarea
          v-model="item.name"
          label="Título*"
          rows="3"
          prepend-icon="mdi-format-title"
          counter="2000"
          :error-messages="getErrorMsgs(v$.item.name)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <v-text-field
          v-model.number="item.weight"
          label="Peso*"
          type="number"
          min="1"
          prepend-icon="mdi-weight"
          hint="Complejidad"
          persistent-hint
          :error-messages="getErrorMsgs(v$.item.weight)"
        />
      </v-col>
      <v-col v-if="item.id" cols="6">
        <v-switch v-model="item.done" label="Terminada*" prepend-icon="mdi-check-bold" inset />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { maxLength, minValue, numeric, required } from "@vuelidate/validators";

import TaskService from "@/modules/scrum/services/task-service";

import useForm, { formProps } from "@/composables/useForm";

export default {
  name: "TaskForm",
  props: formProps,
  validations() {
    return {
      item: {
        name: { required, maxLength: maxLength(2000) },
        weight: { required, numeric, minValue: minValue(1) },
      },
    };
  },
  setup(props) {
    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(props, TaskService, {
      successMessage: "Tarea guardada correctamente",
    });

    return {
      // State
      item,
      // Computed
      v$,
      itemHasChanged,
      isFormLoading,
      // Methods
      getErrorMsgs,
      submit,
      reset,
    };
  },
};
</script>
