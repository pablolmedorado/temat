<template>
  <v-form v-if="item" ref="itemForm" :disabled="isFormLoading">
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.name"
          label="Título*"
          counter="200"
          prepend-icon="mdi-format-title"
          :error-messages="getErrorMsgs(v$.item.name)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6">
        <DatePickerInput
          v-model="startDate"
          label="Fecha de inicio*"
          prepend-icon="mdi-calendar-start"
          :error-messages="getErrorMsgs(v$.startDate)"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <DatePickerInput
          v-model="endDate"
          label="Fecha de fin*"
          prepend-icon="mdi-calendar-end"
          :error-messages="getErrorMsgs(v$.endDate)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-switch v-model="item.all_day" label="Todo el día" inset />
      </v-col>
    </v-row>
    <v-row v-show="!item.all_day">
      <v-col cols="12" sm="6">
        <TimePickerInput
          v-model="startTime"
          label="Hora de inicio"
          prepend-icon="mdi-clock-start"
          :disabled="item.all_day"
          :error-messages="getErrorMsgs(v$.startTime)"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <TimePickerInput
          v-model="endTime"
          label="Hora de fin"
          prepend-icon="mdi-clock-end"
          :disabled="item.all_day"
          :error-messages="getErrorMsgs(v$.endTime)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="6">
        <v-select
          v-model.number="item.type"
          :items="eventTypesOptions.filter((ev) => !ev.system_slug)"
          item-text="name"
          item-value="id"
          label="Tipo de evento*"
          prepend-icon="mdi-shape"
          :loading="!eventTypesOptions.length"
          :error-messages="getErrorMsgs(v$.item.type)"
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-select
          v-model.number="item.visibility"
          :items="visibilityOptions"
          item-text="label"
          item-value="value"
          label="Visibilidad*"
          prepend-icon="mdi-eye"
          :loading="!visibilityOptions.length"
          :error-messages="getErrorMsgs(v$.item.visibility)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-text-field
          v-model="item.location"
          label="Ubicación"
          counter="200"
          prepend-icon="mdi-map-marker"
          :error-messages="getErrorMsgs(v$.item.location)"
        >
          <template #append>
            <v-icon v-show="item.location" @click="openLocation(item.location)">mdi-google-maps</v-icon>
          </template>
        </v-text-field>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <v-textarea
          v-model="item.details"
          label="Detalles"
          counter="2000"
          prepend-icon="mdi-text"
          :error-messages="getErrorMsgs(v$.item.details)"
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <UserAutocomplete
          v-model="item.attendees"
          label="Usuarios asistentes"
          prepend-icon="mdi-account"
          multiple
          chips
          small-chips
          deletable-chips
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <GroupAutocomplete
          v-model="item.groups"
          label="Grupos asistentes"
          prepend-icon="mdi-account-group"
          multiple
          chips
          small-chips
          deletable-chips
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <TagAutocomplete v-model="item.tags" label="Tags" prepend-icon="mdi-label" multiple chips deletable-chips />
      </v-col>
    </v-row>
    <small>* indica campo obligatorio</small>
  </v-form>
</template>

<script>
import { computed, ref, toRefs, watch } from "@vue/composition-api";
import { DateTime } from "luxon";
import { cloneDeep, defaultTo } from "lodash-es";
import { maxLength, required, requiredUnless } from "@vuelidate/validators";

import EventService from "@/modules/calendar/services/event-service";

import { useMainStore } from "@/stores/main";
import { useEventStore } from "@/modules/calendar/stores/events";
import useForm, { formProps } from "@/composables/useForm";

export default {
  name: "EventForm",
  props: formProps,
  validations() {
    return {
      startDate: { required },
      endDate: {
        required,
        endDateBeforeStartDate: (value, siblings) => {
          const startDateAux = DateTime.fromISO(siblings.startDate);
          const endDateAux = DateTime.fromISO(value);
          return endDateAux.diff(startDateAux).milliseconds >= 0;
        },
      },
      startTime: { required: requiredUnless(this.item.all_day) },
      endTime: {
        required: requiredUnless(this.item.all_day),
        endTimeBeforeStartTime: (value, siblings) => {
          return (
            siblings.startDate !== siblings.endDate ||
            siblings.endDateTime.diff(siblings.startDateTime).milliseconds >= 0
          );
        },
      },
      item: {
        name: { required, maxLength: maxLength(200) },
        type: { required },
        visibility: { required },
        details: { maxLength: maxLength(2000) },
        location: { maxLength: maxLength(200) },
      },
    };
  },
  setup(props) {
    // Store
    const mainStore = useMainStore();
    const eventStore = useEventStore();

    // State
    const startDate = ref(DateTime.fromISO(props.sourceItem.start_datetime).toISODate());
    const endDate = ref(DateTime.fromISO(props.sourceItem.end_datetime).toISODate());
    const startTime = ref(DateTime.fromISO(props.sourceItem.start_datetime).toFormat("HH:mm"));
    const endTime = ref(DateTime.fromISO(props.sourceItem.end_datetime).toFormat("HH:mm"));

    // Composables
    const { v$, getErrorMsgs, item, itemHasChanged, submit, reset, isFormLoading } = useForm(props, EventService, {
      initializeItem,
      buildSaveFunctionArgs,
      successMessage: "Evento guardado correctamente",
      customErrorMsgs: {
        endDateBeforeStartDate: "Fecha de fin anterior a la de inicio",
        endTimeBeforeStartTime: "Hora de fin anterior a la de inicio",
      },
    });

    // Computed
    const { locale } = toRefs(mainStore);
    const { eventTypes: eventTypesOptions, eventVisibilityTypes: visibilityOptions } = toRefs(eventStore);
    const startDateTime = computed(() => {
      return DateTime.fromFormat(`${startDate.value} ${defaultTo(startTime.value, "00:00")}`, "yyyy-MM-dd HH:mm");
    });
    const endDateTime = computed(() => {
      return DateTime.fromFormat(`${endDate.value} ${defaultTo(endTime.value, "00:00")}`, "yyyy-MM-dd HH:mm");
    });

    // Watchers
    watch(startDateTime, (newDateTime, oldDateTime) => {
      const previousDiff = endDateTime.value.diff(oldDateTime);
      const newEndDateTime = newDateTime.plus(previousDiff);
      endDate.value = newEndDateTime.toISODate();
      endTime.value = newEndDateTime.toFormat("HH:mm");
    });

    // Methods
    function initializeItem(newItem) {
      startDate.value = DateTime.fromISO(newItem.start_datetime).toISODate();
      endDate.value = DateTime.fromISO(newItem.end_datetime).toISODate();
      startTime.value = DateTime.fromISO(newItem.start_datetime).toFormat("HH:mm");
      endTime.value = DateTime.fromISO(newItem.end_datetime).toFormat("HH:mm");

      const item = cloneDeep(newItem);
      item.tags = newItem.tags.map((tag) => tag.name);
      return item;
    }
    function buildSaveFunctionArgs(cleanedItem) {
      const payload = {
        ...cleanedItem,
        start_datetime: startDateTime.value.toISO(),
        end_datetime: endDateTime.value.toISO(),
      };
      return [payload, { expand: "tags" }];
    }
    function openLocation(location) {
      window.open(`https://www.google.com/maps/search/${location}/`, "_blank");
    }

    return {
      // State
      item,
      startDate,
      endDate,
      startTime,
      endTime,
      // Computed
      v$,
      itemHasChanged,
      isFormLoading,
      locale,
      eventTypesOptions,
      visibilityOptions,
      startDateTime,
      endDateTime,
      // Methods
      getErrorMsgs,
      submit,
      reset,
      openLocation,
    };
  },
};
</script>
