<template>
  <form v-if="item" ref="itemForm">
    <v-container>
      <v-row>
        <v-col>
          <v-text-field
            v-model="item.name"
            label="Nombre*"
            prepend-icon="mdi-format-title"
            counter="200"
            :error-messages="buildValidationErrorMessages($v.item.name)"
            @input="$v.item.name.$touch()"
            @blur="$v.item.name.$touch()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-textarea
            v-model="item.description"
            label="Descripción"
            prepend-icon="mdi-text"
            counter="2000"
            :error-messages="buildValidationErrorMessages($v.item.description)"
            @input="$v.item.description.$touch()"
            @blur="$v.item.description.$touch()"
          ></v-textarea>
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
            :error-messages="buildValidationErrorMessages($v.item.external_reference)"
            @input="$v.item.external_reference.$touch()"
            @blur="$v.item.external_reference.$touch()"
          ></v-text-field>
        </v-col>
      </v-row>
      <small>* indica campo obligatorio</small>
    </v-container>
  </form>
</template>

<script>
import { maxLength, required } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import EpicService from "@/services/scrum/epic-service";

export default {
  name: "EpicForm",
  mixins: [FormMixin({ service: EpicService })],
  validations: {
    item: {
      name: { required, maxLength: maxLength(200) },
      description: { maxLength: maxLength(2000) },
      external_reference: { maxLength: maxLength(2000) },
    },
  },
  data() {
    return {
      successMessage: "Épica guardada correctamente",
    };
  },
};
</script>
