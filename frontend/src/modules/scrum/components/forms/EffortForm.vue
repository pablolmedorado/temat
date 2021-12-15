<template>
  <v-form v-if="item" ref="itemForm" :disabled="isTaskLoading('submit')">
    <v-row>
      <v-col>
        <DatePickerInput
          v-model="item.date"
          label="Fecha*"
          prepend-icon="mdi-calendar"
          :max="today"
          :error-messages="buildValidationErrorMessages($v.item.date)"
          @input="$v.item.date.$touch()"
          @blur="$v.item.date.$touch()"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-select
          v-model.trim="item.role"
          :items="effortRoleOptions"
          item-text="label"
          item-value="value"
          label="Rol*"
          prepend-icon="mdi-badge-account"
          :loading="!effortRoleOptions.length"
          :error-messages="buildValidationErrorMessages($v.item.role)"
          @change="$v.item.role.$touch()"
          @blur="$v.item.role.$touch()"
        />
      </v-col>
      <v-col>
        <v-text-field
          v-model.number="item.effort"
          label="Esfuerzo*"
          type="number"
          min="1"
          prepend-icon="mdi-dumbbell"
          suffix="UT"
          hint="1UT = 1/2h"
          persistent-hint
          :error-messages="buildValidationErrorMessages($v.item.effort)"
          @input="$v.item.effort.$touch()"
          @blur="$v.item.effort.$touch()"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-textarea
          v-model="item.comments"
          label="Comentarios"
          prepend-icon="mdi-comment-quote"
          counter="2000"
          :error-messages="buildValidationErrorMessages($v.item.comments)"
          @input="$v.item.comments.$touch()"
          @blur="$v.item.comments.$touch()"
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { mapState } from "pinia";
import { DateTime } from "luxon";
import { isObject } from "lodash";
import { maxLength, minValue, numeric, required } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import EffortService from "@/modules/scrum/services/effort-service";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

export default {
  name: "EffortForm",
  mixins: [FormMixin({ service: EffortService })],
  validations: {
    item: {
      date: {
        required,
        noFutureAllocations: (value) => {
          return DateTime.fromISO(value) < DateTime.local();
        },
      },
      role: { required },
      effort: { required, numeric, minValue: minValue(1) },
      comments: { maxLength: maxLength(2000) },
    },
  },
  data() {
    return {
      today: DateTime.local().toISODate(),
      successMessage: "Esfuerzo guardado correctamente",
      validationErrorMessages: {
        noFutureAllocations: "No es posible imputar a futuro",
      },
    };
  },
  computed: {
    ...mapState(useUserStoryStore, {
      effortRoleOptions: "effortRoles",
    }),
  },
  methods: {
    buildSaveFunctionArgs() {
      return [
        this.replaceUndefined({
          ...this.item,
          user_story: isObject(this.item.user_story) ? this.item.user_story.id : this.item.user_story,
        }),
      ];
    },
  },
};
</script>
