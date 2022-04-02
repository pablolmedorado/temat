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
import { computed, onActivated, ref, toRefs, watch } from "@vue/composition-api";
import { DateTime, Interval } from "luxon";
import { debounce, defaultTo, sortBy } from "lodash-es";
import { escapeHTML } from "vuetify/es5/util/helpers";

import CalendarEvent from "@/modules/calendar/models/event";

import EventService from "@/modules/calendar/services/event-service";

import EventCard from "@/modules/calendar/components/EventCard";
import EventForm from "@/modules/calendar/components/forms/EventForm";

import { useMainStore } from "@/stores/main";

import useEventTypes from "@/modules/calendar/composables/useEventTypes";
import useLoading from "@/composables/useLoading";
import useLocalStorage from "@/composables/useLocalStorage";
import { getFontColourFromBackground, hex2rgba } from "@/utils/colours";

export default {
  name: "CalendarView",
  metaInfo() {
    return {
      title: `${this.calendarIntervalRepresentation} - Calendario`,
    };
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
  setup(props, { refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();
    const { eventTypesMap } = useEventTypes();

    // State
    const calendarType = useLocalStorage("calendarType", "month");
    const excludeSystemEvents = useLocalStorage("calendarExcludeSystemEvents", false);
    const referenceDate = ref(defaultTo(props.initialDate, DateTime.local().toISODate()));
    const events = ref([]);
    const typeOptions = [
      { text: "Día", value: "day", icon: "mdi-view-day" },
      { text: "Semana", value: "week", icon: "mdi-view-week" },
      { text: "Mes", value: "month", icon: "mdi-view-comfy" },
    ];
    const typeToLabel = {
      month: "Mes",
      week: "Semana",
      day: "Día",
    };
    const weekdays = [1, 2, 3, 4, 5, 6, 0];
    const showDatePicker = ref(false);
    const formComponent = EventForm;
    const selectedEvent = ref(null);
    const showEventCard = ref(false);

    // Computed
    const { locale } = toRefs(store);
    const pickerDate = computed({
      get() {
        if (calendarType.value === "month") {
          return DateTime.fromISO(referenceDate.value).toFormat("y-MM");
        }
        return referenceDate.value;
      },
      set(value) {
        referenceDate.value = DateTime.fromISO(value).toISODate();
      },
    });
    const calendarInterval = computed(() => {
      const dateTime = DateTime.fromISO(referenceDate.value);
      const startDate = dateTime.startOf(calendarType.value);
      const endDate = dateTime.endOf(calendarType.value);
      return Interval.fromDateTimes(startDate, endDate);
    });
    const calendarIntervalRepresentation = computed(() =>
      DateTime.fromISO(referenceDate.value)
        .setLocale(locale.value)
        .toFormat(calendarType.value === "week" ? "'W'W (MMMM yyyy)" : "MMMM yyyy")
    );

    // Watchers
    watch(
      () => props.initialDate,
      (newValue) => {
        if (newValue) {
          referenceDate.value = newValue;
        }
      }
    );
    watch(excludeSystemEvents, fetchEvents);

    // Methods
    const onCalendarChange = debounce(function () {
      events.value = [];
      fetchEvents();
    }, 500);
    function onTypeChange(type) {
      calendarType.value = type;
    }
    function onDateClick({ date }) {
      referenceDate.value = date;
      calendarType.value = "day";
    }
    function onDayClick({ date }) {
      refs.formDialog.open({
        ...CalendarEvent.getDefaults(),
        start_datetime: DateTime.fromISO(date).toISO(),
        end_datetime: DateTime.fromISO(date).toISO(),
      });
    }
    function onEventClick({ nativeEvent, event }) {
      const open = () => {
        selectedEvent.value = {
          data: event,
          htmlElement: nativeEvent.target,
        };
        setTimeout(() => (showEventCard.value = true), 10);
      };

      if (showEventCard.value) {
        showEventCard.value = false;
        setTimeout(open, 10);
      } else {
        open();
      }

      nativeEvent.stopPropagation();
    }
    function onNewEventClick() {
      const newEventData = { ...CalendarEvent.getDefaults() };
      if (calendarType.value === "day") {
        const dateTime = DateTime.fromISO(referenceDate.value).toISO();
        newEventData.start_datetime = dateTime;
        newEventData.end_datetime = dateTime;
      }
      refs.formDialog.open(newEventData);
    }
    async function fetchEvents() {
      addTask("fetch-events");
      try {
        events.value = await EventService.listCalendar(calendarInterval.value, excludeSystemEvents.value);
      } finally {
        removeTask("fetch-events");
      }
    }
    function addOrUpdateEvent(event) {
      const eventsCopy = [...events.value];
      const eventIndex = eventsCopy.findIndex((item) => item.id === event.id);
      if (eventIndex !== -1) {
        eventsCopy.splice(eventIndex, 1, event);
      } else {
        eventsCopy.push(event);
      }
      events.value = sortBy(eventsCopy, ["start_datetime", "name"]);
    }
    function removeEvent(event) {
      const eventIndex = events.value.findIndex((item) => item.id === event.id);
      if (eventIndex !== -1) {
        events.value.splice(eventIndex, 1);
      }
    }
    function onSaveEvent(eventData) {
      selectedEvent.value = null;
      const event = new CalendarEvent(eventData);
      if (calendarInterval.value.overlaps(event.luxonInterval)) {
        addOrUpdateEvent(event);
      } else {
        removeEvent(event);
      }
    }
    function onDeleteEvent(event) {
      selectedEvent.value = null;
      removeEvent(event);
      store.showSnackbar({ color: "success", message: "Evento eliminado correctamente" });
    }
    function setEventName(event) {
      const name = escapeHTML(event.input.name);
      const icon = `<i aria-hidden="true" class="v-icon notranslate mdi ${
        eventTypesMap.value[event.input.type].icon
      } calendar-event-icon"></i>`;
      return `${icon} ${name}`;
    }
    function setEventColour(event) {
      const alpha = event.luxonEnd < DateTime.local() ? ".5" : "1";
      return hex2rgba(eventTypesMap.value[event.type].colour, alpha);
    }
    function setEventFontColour(event) {
      const alpha = event.luxonEnd < DateTime.local() ? ".54" : "1";
      return getFontColourFromBackground(eventTypesMap.value[event.type].colour, alpha);
    }
    function setIntervalStyle(interval) {
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
    }
    function setToday() {
      referenceDate.value = DateTime.local().toISODate();
    }

    // Lifecycle hooks
    onActivated(() => fetchEvents());

    return {
      // State
      eventTypesMap,
      calendarType,
      excludeSystemEvents,
      referenceDate,
      events,
      typeOptions,
      typeToLabel,
      weekdays,
      showDatePicker,
      formComponent,
      selectedEvent,
      showEventCard,
      // Computed
      isLoading,
      locale,
      pickerDate,
      calendarIntervalRepresentation,
      // Methods
      isTaskLoading,
      fetchEvents,
      onCalendarChange,
      onTypeChange,
      onDateClick,
      onDayClick,
      onEventClick,
      onNewEventClick,
      onSaveEvent,
      onDeleteEvent,
      setEventName,
      setEventColour,
      setEventFontColour,
      setIntervalStyle,
      setToday,
    };
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
