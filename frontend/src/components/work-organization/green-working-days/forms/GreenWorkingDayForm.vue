<template>
  <form v-if="item" ref="itemForm">
    <v-container>
      <v-row>
        <v-col>
          <v-text-field
            v-model="item.label"
            label="Etiqueta"
            prepend-icon="mdi-tag"
            counter="100"
            :error-messages="buildValidationErrorMessages($v.item.label)"
            @input="$v.item.label.$touch()"
            @blur="$v.item.label.$touch()"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6">
          <UserAutocomplete
            v-model.number="item.main_user"
            label="Usuario principal"
            prepend-icon="mdi-account"
            :limit-random-choices-to="item.volunteers"
            show-random-btn
          />
        </v-col>
        <v-col cols="12" sm="6">
          <UserAutocomplete
            v-model.number="item.support_user"
            label="Usuario de apoyo"
            prepend-icon="mdi-account-outline"
            :limit-random-choices-to="item.volunteers"
            show-random-btn
            :error-messages="buildValidationErrorMessages($v.item.support_user)"
            @change="$v.item.support_user.$touch()"
            @blur="$v.item.support_user.$touch()"
          />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <UserAutocomplete
            v-model="item.volunteers"
            label="Usuarios voluntarios"
            prepend-icon="mdi-account-multiple"
            multiple
            chips
            small-chips
            deletable-chips
          />
        </v-col>
      </v-row>
    </v-container>
  </form>
</template>

<script>
import { mapState } from "vuex";
import { maxLength, not, sameAs } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import GreenService from "@/services/work-organization/green-service";

export default {
  name: "GreenWorkingDayForm",
  mixins: [FormMixin({ service: GreenService })],
  validations: {
    item: {
      label: { maxLength: maxLength(100) },
      support_user: { notSameAsMainUser: not(sameAs("main_user")) },
    },
  },
  data() {
    return {
      saveFunctionName: "update",
      validationErrorMessages: {
        notSameAsMainUser: "Usuario repetido",
      },
      successMessage: "Jornada especial guardada correctamente",
    };
  },
  computed: {
    ...mapState("users", {
      userOptions: "users",
    }),
  },
};
</script>
