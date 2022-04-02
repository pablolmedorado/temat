<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <DatePickerInput
          v-model="item.date"
          label="Fecha*"
          prepend-icon="mdi-calendar"
          :max="today"
          :error-messages="getErrorMsgs(v$.item.date)"
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
          :error-messages="getErrorMsgs(v$.item.role)"
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
          :error-messages="getErrorMsgs(v$.item.effort)"
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
          :error-messages="getErrorMsgs(v$.item.comments)"
        />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { toRefs } from "@vue/composition-api";
import { DateTime } from "luxon";
import { isObject } from "lodash-es";
import { maxLength, minValue, numeric, required } from "@vuelidate/validators";

import EffortService from "@/modules/scrum/services/effort-service";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";
import useForm, { formProps } from "@/composables/useForm";

export default {
  name: "EffortForm",
  props: formProps,
  validations() {
    return {
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
    };
  },
  setup(props) {
    // Store
    const userStoryStore = useUserStoryStore();

    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(props, EffortService, {
      buildSaveFunctionArgs,
      successMessage: "Esfuerzo guardado correctamente",
      customErrorMsgs: {
        noFutureAllocations: "No es posible imputar a futuro",
      },
    });

    // State
    const today = DateTime.local().toISODate();

    // Computed
    const { effortRoles: effortRoleOptions } = toRefs(userStoryStore);

    // Methods
    function buildSaveFunctionArgs(cleanedItem) {
      return [
        {
          ...cleanedItem,
          user_story: isObject(cleanedItem.user_story) ? cleanedItem.user_story.id : cleanedItem.user_story,
        },
      ];
    }

    return {
      // State
      item,
      today,
      // Computed
      v$,
      itemHasChanged,
      isFormLoading,
      effortRoleOptions,
      // Methods
      getErrorMsgs,
      submit,
      reset,
    };
  },
};
</script>
