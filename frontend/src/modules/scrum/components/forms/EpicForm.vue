<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.name"
          label="Nombre*"
          prepend-icon="mdi-format-title"
          counter="200"
          :error-messages="getErrorMsgs(v$.item.name)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-textarea
          v-model="item.description"
          label="Descripción"
          prepend-icon="mdi-text"
          counter="2000"
          :error-messages="getErrorMsgs(v$.item.description)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <TagAutocomplete v-model="item.tags" label="Tags" prepend-icon="mdi-label" multiple chips deletable-chips />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.external_reference"
          label="Referencia externa"
          prepend-icon="mdi-open-in-new"
          counter="2000"
          :error-messages="getErrorMsgs(v$.item.external_reference)"
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { maxLength, required } from "@vuelidate/validators";

import EpicService from "@/modules/scrum/services/epic-service";

import useForm, { formProps } from "@/composables/useForm";

export default {
  name: "EpicForm",
  props: formProps,
  validations() {
    return {
      item: {
        name: { required, maxLength: maxLength(200) },
        description: { maxLength: maxLength(2000) },
        external_reference: { maxLength: maxLength(2000) },
      },
    };
  },
  setup(props) {
    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(props, EpicService, {
      successMessage: "Épica guardada correctamente",
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
