<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" :max-width="maxWidth" persistent scrollable>
    <v-card>
      <v-card-title class="text-h6">
        <slot name="header">Creación múltiple</slot>
      </v-card-title>
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
              />
            </v-stepper-content>
          </v-stepper-items>
        </v-stepper>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-btn color="warning" text @click="reset">Restablecer</v-btn>
        <v-spacer />
        <v-btn color="primary" text @click="close">Cancelar</v-btn>
        <v-btn color="primary" text :disabled="!datesToCreate.length" @click="next">
          {{ nextText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapState } from "vuex";

import DialogMixin from "@/mixins/dialog-mixin";

export default {
  name: "StepperBulkFormDialog",
  mixins: [DialogMixin],
  props: {
    formComponent: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      step: 1,
      datesToCreate: [],
      itemsToCreate: [],
    };
  },
  computed: {
    ...mapState(["locale"]),
    nextText() {
      return this.step < 2 ? "Siguiente" : "Guardar";
    },
  },
  methods: {
    reset() {
      this.datesToCreate = [];
      this.itemsToCreate = [];
      this.step = 1;
    },
    close() {
      this.reset();
      this.showDialog = false;
    },
    step2() {
      this.itemsToCreate = this.datesToCreate.map((date) => {
        return { date, user: null };
      });
      this.step = 2;
    },
    async submit() {
      const newItems = await this.$refs.itemsForm.submit();
      if (newItems) {
        this.$emit("submit", newItems);
        this.close();
      }
    },
    next() {
      this.step < 2 ? this.step2() : this.submit();
    },
  },
};
</script>
