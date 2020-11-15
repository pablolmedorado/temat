<template>
  <form v-if="item" ref="itemForm">
    <v-container>
      <v-row>
        <v-col>
          <v-text-field
            v-model="item.name"
            label="Título*"
            counter="200"
            prepend-icon="mdi-format-title"
            :error-messages="buildValidationErrorMessages($v.item.name)"
            @input="$v.item.name.$touch()"
            @blur="$v.item.name.$touch()"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6">
          <DatePickerInput
            v-model="startDate"
            label="Fecha de inicio*"
            prepend-icon="mdi-calendar-start"
            :error-messages="buildValidationErrorMessages($v.startDate)"
            @input="$v.startDate.$touch()"
            @blur="$v.startDate.$touch()"
          ></DatePickerInput>
        </v-col>
        <v-col cols="12" sm="6">
          <DatePickerInput
            v-model="endDate"
            label="Fecha de fin*"
            prepend-icon="mdi-calendar-end"
            :error-messages="buildValidationErrorMessages($v.endDate)"
            @input="$v.endDate.$touch()"
            @blur="$v.endDate.$touch()"
          ></DatePickerInput>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-switch v-model="item.all_day" label="Todo el día" inset></v-switch>
        </v-col>
      </v-row>
      <v-row v-show="!item.all_day">
        <v-col cols="12" sm="6">
          <v-menu
            ref="startTimepicker"
            v-model="showStartTimepicker"
            :close-on-content-click="false"
            :nudge-right="40"
            :return-value.sync="startTime"
            transition="scale-transition"
            offset-y
            width="290px"
          >
            <template #activator="{ on, attrs }">
              <v-text-field
                v-model="startTime"
                label="Hora de inicio"
                prepend-icon="mdi-clock-start"
                readonly
                :disabled="item.all_day"
                :error-messages="buildValidationErrorMessages($v.startTime)"
                v-bind="attrs"
                v-on="on"
                @blur="$v.startTime.$touch()"
              ></v-text-field>
            </template>
            <v-time-picker
              v-if="showStartTimepicker"
              v-model="startTime"
              format="24hr"
              color="primary"
              scrollable
              @change="$v.startTime.$touch()"
              @click:minute="$refs.startTimepicker.save(startTime)"
            ></v-time-picker>
          </v-menu>
        </v-col>
        <v-col cols="12" sm="6">
          <v-menu
            ref="endTimepicker"
            v-model="showEndTimepicker"
            :close-on-content-click="false"
            :nudge-right="40"
            :return-value.sync="endTime"
            transition="scale-transition"
            offset-y
            width="290px"
          >
            <template #activator="{ on, attrs }">
              <v-text-field
                v-model="endTime"
                label="Hora de fin"
                prepend-icon="mdi-clock-end"
                readonly
                :disabled="item.all_day"
                :error-messages="buildValidationErrorMessages($v.endTime)"
                v-bind="attrs"
                v-on="on"
                @blur="$v.endTime.$touch()"
              ></v-text-field>
            </template>
            <v-time-picker
              v-if="showEndTimepicker"
              v-model="endTime"
              format="24hr"
              color="primary"
              scrollable
              @change="$v.endTime.$touch()"
              @click:minute="$refs.endTimepicker.save(endTime)"
            ></v-time-picker>
          </v-menu>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" sm="6">
          <v-select
            v-model.number="item.type"
            :items="eventTypesOptions.filter((ev) => !ev.system)"
            item-text="name"
            item-value="id"
            label="Tipo de evento*"
            prepend-icon="mdi-shape"
            :loading="!eventTypesOptions.length"
            :error-messages="buildValidationErrorMessages($v.item.type)"
            @change="$v.item.type.$touch()"
            @blur="$v.item.type.$touch()"
          ></v-select>
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
            :error-messages="buildValidationErrorMessages($v.item.visibility)"
            @change="$v.item.visibility.$touch()"
            @blur="$v.item.visibility.$touch()"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-text-field
            v-model="item.location"
            label="Ubicación"
            counter="200"
            prepend-icon="mdi-map-marker"
            append-icon="mdi-google-maps"
            :error-messages="buildValidationErrorMessages($v.item.location)"
            @input="$v.item.location.$touch()"
            @blur="$v.item.location.$touch()"
            @click:append="openLocation(item.location)"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-textarea
            v-model="item.details"
            label="Detalles"
            counter="2000"
            prepend-icon="mdi-text"
            :error-messages="buildValidationErrorMessages($v.item.details)"
            @input="$v.item.details.$touch()"
            @blur="$v.item.details.$touch()"
          ></v-textarea>
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
    </v-container>
  </form>
</template>

<script>
import { mapState, mapActions } from "vuex";
import { DateTime } from "luxon";
import { cloneDeep, defaultTo } from "lodash";
import { maxLength, required, requiredUnless } from "vuelidate/lib/validators";

import FormMixin from "@/mixins/form-mixin";

import EventService from "@/services/calendar/event-service";

export default {
  name: "EventForm",
  mixins: [FormMixin({ service: EventService })],
  validations: {
    startDate: { required },
    endDate: {
      required,
      endDateBeforeStartDate: (value, vm) => {
        const startDateAux = DateTime.fromISO(vm.startDate);
        const endDateAux = DateTime.fromISO(vm.endDate);
        return endDateAux.diff(startDateAux).milliseconds >= 0;
      },
    },
    startTime: { required: requiredUnless("item.all_day") },
    endTime: {
      required: requiredUnless("item.all_day"),
      endTimeBeforeStartTime: (value, vm) => {
        return vm.startDate !== vm.endDate || vm.endDateTime.diff(vm.startDateTime).milliseconds >= 0;
      },
    },
    item: {
      name: { required, maxLength: maxLength(200) },
      type: { required },
      visibility: { required },
      details: { maxLength: maxLength(2000) },
      location: { maxLength: maxLength(200) },
    },
  },
  data() {
    return {
      startDate: DateTime.fromISO(this.sourceItem.start_datetime).toISODate(),
      endDate: DateTime.fromISO(this.sourceItem.end_datetime).toISODate(),
      startTime: DateTime.fromISO(this.sourceItem.start_datetime).toFormat("HH:mm"),
      endTime: DateTime.fromISO(this.sourceItem.end_datetime).toFormat("HH:mm"),
      showStartTimepicker: false,
      showEndTimepicker: false,
      validationErrorMessages: {
        endDateBeforeStartDate: "Fecha de fin anterior a la de inicio",
        endTimeBeforeStartTime: "Hora de fin anterior a la de inicio",
      },
      successMessage: "Evento guardado correctamente",
    };
  },
  computed: {
    ...mapState(["locale"]),
    ...mapState("users", {
      attendeesOptions: "users",
      groupsOptions: "groups",
    }),
    ...mapState("calendar", {
      eventTypesOptions: "eventTypes",
      visibilityOptions: "eventVisibilityTypes",
    }),
    startDateTime() {
      return DateTime.fromFormat(`${this.startDate} ${defaultTo(this.startTime, "00:00")}`, "yyyy-MM-dd HH:mm");
    },
    endDateTime() {
      return DateTime.fromFormat(`${this.endDate} ${defaultTo(this.endTime, "00:00")}`, "yyyy-MM-dd HH:mm");
    },
  },
  watch: {
    startDateTime: {
      handler(newDateTime, oldDateTime) {
        const previousDiff = this.endDateTime.diff(oldDateTime);
        const newEndDateTime = newDateTime.plus(previousDiff);
        this.endDate = newEndDateTime.toISODate();
        this.endTime = newEndDateTime.toFormat("HH:mm");
      },
    },
  },
  methods: {
    ...mapActions("calendar", ["saveEvent"]),
    initializeItem(newItem) {
      this.startDate = DateTime.fromISO(newItem.start_datetime).toISODate();
      this.endDate = DateTime.fromISO(newItem.end_datetime).toISODate();
      this.startTime = DateTime.fromISO(newItem.start_datetime).toFormat("HH:mm");
      this.endTime = DateTime.fromISO(newItem.end_datetime).toFormat("HH:mm");
      return cloneDeep(newItem);
    },
    openLocation(location) {
      window.open(`https://www.google.com/maps/search/${location}/`, "_blank");
    },
    buildSaveFunctionArgs() {
      const payload = {
        ...this.item,
        start_datetime: this.startDateTime.toISO(),
        end_datetime: this.endDateTime.toISO(),
      };
      return [this.replaceUndefined(payload)];
    },
  },
};
</script>
