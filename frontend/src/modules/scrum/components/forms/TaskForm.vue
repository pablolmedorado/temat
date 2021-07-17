<template>
  <form v-if="item" ref="itemForm">
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.name"
          label="Título*"
          prepend-icon="mdi-format-title"
          counter="2000"
          :error-messages="buildValidationErrorMessages($v.item.name)"
          @input="$v.item.name.$touch()"
          @blur="$v.item.name.$touch()"
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
          :error-messages="buildValidationErrorMessages($v.item.weight)"
          @input="$v.item.weight.$touch()"
          @blur="$v.item.weight.$touch()"
        />
      </v-col>
      <v-col v-if="item.id" cols="6">
        <v-switch v-model="item.done" label="Terminada*" prepend-icon="mdi-check-bold" inset />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </form>
</template>

<script>
import { maxLength, minValue, numeric, required } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import TaskService from "@/modules/scrum/services/task-service";

export default {
  name: "TaskForm",
  mixins: [FormMixin({ service: TaskService })],
  validations: {
    item: {
      name: { required, maxLength: maxLength(2000) },
      weight: { required, numeric, minValue: minValue(1) },
    },
  },
  data() {
    return {
      successMessage: "Tarea guardada correctamente",
    };
  },
};
</script>
