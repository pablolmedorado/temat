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
              :error-messages="buildValidationErrorMessages($v.newQuickFilter)"
              @change="$v.newQuickFilter.$touch()"
              @blur="$v.newQuickFilter.$touch()"
            />
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-alert type="warning" border="left" text outlined>
              Los filtros rápidos se almacenan en el navegador y se pierden al cerrar sesión.
            </v-alert>
          </v-col>
        </v-row>
        <small>* indica campo obligatorio</small>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn color="primary" text @click.stop="close"> Volver </v-btn>
        <v-btn color="primary" text :disabled="$v.$invalid" @click="addQuickFilter">
          {{ isObject(newQuickFilter) ? "Actualizar" : "Guardar" }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { isObject } from "lodash";
import { validationMixin } from "vuelidate";
import { required } from "vuelidate/lib/validators";

import DialogMixin from "@/mixins/dialog-mixin";

import { buildValidationErrorMessages, validationErrorMessages } from "@/utils/validation";

export default {
  name: "QuickFilterDialog",
  mixins: [DialogMixin, validationMixin],
  props: {
    quickFilters: {
      type: Array,
      required: true,
    },
  },
  validations: {
    newQuickFilter: { required },
  },
  data() {
    return {
      validationErrorMessages,
      newQuickFilter: undefined,
    };
  },
  watch: {
    showDialog() {
      this.newQuickFilter = undefined;
      this.$v.$reset();
    },
  },
  methods: {
    isObject,
    buildValidationErrorMessages,
    addQuickFilter() {
      this.$nextTick(() => {
        this.$emit("add:quick-filter", this.newQuickFilter);
        this.close();
      });
    },
  },
};
</script>
