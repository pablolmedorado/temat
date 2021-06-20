<template>
  <v-container fluid>
    <v-row>
      <v-toolbar flat color="transparent">
        <v-btn outlined class="mr-4" @click="setToday">Hoy</v-btn>
        <v-btn fab text small @click="$refs.calendar.prev()">
          <v-icon>mdi-chevron-left</v-icon>
        </v-btn>
        <v-btn fab text small class="mr-4" @click="$refs.calendar.next()">
          <v-icon>mdi-chevron-right</v-icon>
        </v-btn>
        <v-menu
          v-model="showDatePicker"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="290px"
        >
          <template #activator="{ on, attrs }">
            <v-toolbar-title class="capitalize" v-bind="attrs" v-on="on">
              {{ calendarIntervalRepresentation }}
            </v-toolbar-title>
          </template>
          <v-date-picker
            v-model="pickerDate"
            :type="calendarType == 'month' ? calendarType : 'date'"
            :locale="locale"
            :locale-first-day-of-year="4"
            first-day-of-week="1"
            show-week
            no-title
            @input="showDatePicker = false"
          />
        </v-menu>

        <v-spacer />

        <v-btn fab text small class="mr-2" :disabled="isLoading" @click="fetchEvents">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
        <v-btn fab text small class="mr-2" :to="{ name: 'events' }">
          <v-icon>mdi-magnify</v-icon>
        </v-btn>
        <v-menu bottom right offset-y>
          <template #activator="{ on, attrs }">
            <v-btn class="mr-2" outlined :disabled="isLoading" v-bind="attrs" v-on="on">
              <v-icon left>{{ excludeSystemEvents ? "mdi-eye-off" : "mdi-eye" }}</v-icon>
              <span>E. Sistema</span>
              <v-icon right>mdi-menu-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="excludeSystemEvents = false">
              <v-list-item-icon><v-icon>mdi-eye</v-icon></v-list-item-icon>
              <v-list-item-content><v-list-item-title>Mostrar</v-list-item-title></v-list-item-content>
            </v-list-item>
            <v-list-item @click="excludeSystemEvents = true">
              <v-list-item-icon><v-icon>mdi-eye-off</v-icon></v-list-item-icon>
              <v-list-item-content><v-list-item-title>Ocultar</v-list-item-title></v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
        <v-menu bottom right offset-y>
          <template #activator="{ on, attrs }">
            <v-btn outlined :disabled="isLoading" v-bind="attrs" v-on="on">
              <span>{{ typeToLabel[calendarType] }}</span>
              <v-icon right>mdi-menu-down</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item v-for="(item, index) in typeOptions" :key="index" @click="onTypeChange(item.value)">
              <v-list-item-icon>
                <v-icon>{{ item.icon }}</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>{{ item.text }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
    </v-row>
    <v-row>
      <v-col>
        <v-sheet height="680">
          <v-calendar
            v-if="Object.keys(eventTypesMap).length"
            ref="calendar"
            v-model="referenceDate"
            :events="events"
            :event-color="setEventColour"
            :event-text-color="setEventFontColour"
            :event-name="setEventName"
            :interval-style="setIntervalStyle"
            :short-intervals="false"
            :short-weekdays="false"
            :type="calendarType"
            :weekdays="weekdays"
            :locale-first-day-of-year="4"
            :locale="locale"
            show-week
            color="accent"
            @change="onCalendarChange"
            @click:event="onEventClick"
            @click:date="onDateClick"
            @click:day="onDayClick"
            @click:more="onDateClick"
          />
        </v-sheet>
      </v-col>
    </v-row>

    <v-menu
      v-if="selectedEvent"
      v-model="showEventCard"
      :close-on-content-click="false"
      :activator="selectedEvent.htmlElement"
      :max-width="600"
      offset-x
    >
      <EventCard
        :item="selectedEvent.data"
        :width="600"
        dialog
        @close:dialog="showEventCard = false"
        @update:event="onSaveEvent"
        @delete:event="onDeleteEvent"
      />
    </v-menu>

    <v-btn fab fixed bottom right color="secondary" @click.stop="onNewEventClick">
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <FormDialog ref="formDialog" verbose-name="evento" :form-component="formComponent" @submit="onSaveEvent" />
  </v-container>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { DateTime, Interval } from "luxon";
import { debounce, defaultTo, sortBy } from "lodash";
import { escapeHTML } from "vuetify/es5/util/helpers";

import CalendarEvent from "@/models/event";

import EventService from "@/services/calendar/event-service";

import EventCard from "@/components/calendar/EventCard";
import EventForm from "@/components/calendar/forms/EventForm";

import useLoading from "@/composables/useLoading";
import useLocalStorage from "@/composables/useLocalStorage";
import { getFontColourFromBackground, hex2rgba } from "@/utils/colours";

export default {
  name: "Calendar",
  metaInfo: {
    title: "Calendario",
  },
  components: { EventCard },
  props: {
    initialDate: {
      type: String,
      default: undefined,
      validator: function (value) {
        return DateTime.fromISO(value).isValid;
      },
    },
  },
  setup() {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();

    const calendarType = useLocalStorage("calendarType", "month");
    const excludeSystemEvents = useLocalStorage("calendarExcludeSystemEvents", false);

    return {
      isLoading,
      isTaskLoading,
      addTask,
      removeTask,
      calendarType,
      excludeSystemEvents,
    };
  },
  data() {
    return {
      referenceDate: defaultTo(this.initialDate, DateTime.local().toISODate()),
      events: [],
      typeOptions: [
        { text: "Día", value: "day", icon: "mdi-view-day" },
        { text: "Semana", value: "week", icon: "mdi-view-week" },
        { text: "Mes", value: "month", icon: "mdi-view-comfy" },
      ],
      typeToLabel: {
        month: "Mes",
        week: "Semana",
        day: "Día",
      },
      weekdays: [1, 2, 3, 4, 5, 6, 0],
      showDatePicker: false,
      formComponent: EventForm,
      selectedEvent: null,
      showEventCard: false,
    };
  },
  computed: {
    ...mapState(["locale", "loggedUser"]),
    ...mapGetters("calendar", ["eventTypesMap"]),
    pickerDate: {
      get() {
        if (this.calendarType === "month") {
          return DateTime.fromISO(this.referenceDate).toFormat("y-MM");
        }
        return this.referenceDate;
      },
      set(value) {
        this.referenceDate = DateTime.fromISO(value).toISODate();
      },
    },
    calendarInterval() {
      const dateTime = DateTime.fromISO(this.referenceDate);
      const startDate = dateTime.startOf(this.calendarType);
      const endDate = dateTime.endOf(this.calendarType);
      return Interval.fromDateTimes(startDate, endDate);
    },
    calendarIntervalRepresentation() {
      return DateTime.fromISO(this.referenceDate)
        .setLocale(this.locale)
        .toFormat(this.calendarType === "week" ? "'W'W (MMMM yyyy)" : "MMMM yyyy");
    },
  },
  watch: {
    initialDate(newValue) {
      if (newValue) {
        this.referenceDate = newValue;
      }
    },
    excludeSystemEvents() {
      this.fetchEvents();
    },
  },
  created() {
    if (!Object.keys(this.eventTypesMap).length) {
      this.fetchEventTypes();
    }
  },
  activated() {
    this.fetchEvents();
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    ...mapActions("calendar", ["fetchEventTypes"]),
    onCalendarChange: debounce(function () {
      this.events = [];
      this.fetchEvents();
    }, 500),
    onTypeChange(type) {
      this.calendarType = type;
    },
    onDateClick({ date }) {
      this.referenceDate = date;
      this.calendarType = "day";
    },
    onDayClick({ date }) {
      this.$refs.formDialog.open({
        ...CalendarEvent.defaults,
        start_datetime: DateTime.fromISO(date).toISO(),
        end_datetime: DateTime.fromISO(date).toISO(),
      });
    },
    onEventClick({ nativeEvent, event }) {
      const open = () => {
        this.selectedEvent = {
          data: event,
          htmlElement: nativeEvent.target,
        };
        setTimeout(() => (this.showEventCard = true), 10);
      };

      if (this.showEventCard) {
        this.showEventCard = false;
        setTimeout(open, 10);
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    },
    onNewEventClick() {
      const newEventData = { ...CalendarEvent.defaults };
      if (this.calendarType === "day") {
        const dateTime = DateTime.fromISO(this.referenceDate).toISO();
        newEventData.start_datetime = dateTime;
        newEventData.end_datetime = dateTime;
      }
      this.$refs.formDialog.open(newEventData);
    },
    async fetchEvents() {
      this.addTask("fetch-events");
      try {
        const events = await EventService.listCalendar(this.calendarInterval, this.excludeSystemEvents);
        this.events = events;
      } finally {
        this.removeTask("fetch-events");
      }
    },
    addOrUpdateEvent(event) {
      const eventsCopy = [...this.events];
      const eventIndex = eventsCopy.findIndex((item) => item.id === event.id);
      if (eventIndex !== -1) {
        eventsCopy.splice(eventIndex, 1, event);
      } else {
        eventsCopy.push(event);
      }
      this.events = sortBy(eventsCopy, ["start_datetime", "name"]);
    },
    removeEvent(event) {
      const eventIndex = this.events.findIndex((item) => item.id === event.id);
      if (eventIndex !== -1) {
        this.events.splice(eventIndex, 1);
      }
    },
    onSaveEvent(eventData) {
      this.selectedEvent = null;
      const event = new CalendarEvent(eventData);
      if (this.calendarInterval.overlaps(event.luxonInterval)) {
        this.addOrUpdateEvent(event);
      } else {
        this.removeEvent(event);
      }
    },
    onDeleteEvent(event) {
      this.selectedEvent = null;
      this.removeEvent(event);
      this.showSnackbar({ color: "success", message: "Evento eliminado correctamente" });
    },
    setEventName(event) {
      const name = escapeHTML(event.input.name);
      const icon = `<i aria-hidden="true" class="v-icon notranslate mdi ${
        this.eventTypesMap[event.input.type].icon
      } calendar-event-icon"></i>`;
      return `${icon} ${name}`;
    },
    setEventColour(event) {
      const alpha = event.luxonEnd < DateTime.local() ? ".5" : "1";
      return hex2rgba(this.eventTypesMap[event.type].colour, alpha);
    },
    setEventFontColour(event) {
      const alpha = event.luxonEnd < DateTime.local() ? ".54" : "1";
      return getFontColourFromBackground(this.eventTypesMap[event.type].colour, alpha);
    },
    setIntervalStyle(interval) {
      const inactive =
        interval.weekday === 6 ||
        interval.weekday === 0 ||
        (interval.weekday >= 1 && interval.weekday <= 4 && (interval.hour < 8 || interval.hour >= 17)) ||
        (interval.weekday === 5 && (interval.hour < 7 || interval.hour >= 15));
      const startOfHour = interval.minute === 0;

      const dark = this.dark;
      const backgroundColor = dark ? "rgba(0,0,0,0.4)" : "rgba(0,0,0,0.05)";
      const borderColor = dark ? "rgba(255,255,255,0.1)" : "rgba(0,0,0,0.1)";

      return {
        backgroundColor: inactive ? backgroundColor : undefined,
        borderTop: startOfHour ? undefined : `1px dashed ${borderColor}`,
      };
    },
    setToday() {
      this.referenceDate = DateTime.local().toISODate();
    },
  },
};
</script>

<style scoped>
.capitalize {
  text-transform: capitalize;
}
::v-deep .calendar-event-icon {
  font-size: 12px;
}
</style>
