<template>
  <v-container fluid>
    <v-row v-show="!isLoading">
      <v-col>
        <v-alert v-if="!Object.keys(eventsMap).length" type="info" text outlined border="left">
          No existen eventos futuros en los que figures como invitado.
        </v-alert>
        <v-timeline v-else-if="Object.keys(eventTypesMap).length" align-top :dense="$vuetify.breakpoint.smAndDown">
          <v-timeline-item fill-dot class="mb-5" color="secondary" large>
            <template #icon>
              <v-icon dark>mdi-calendar-today</v-icon>
            </template>
            <span class="font-weight-thin">
              (Se muestran los próximos 10 eventos en los que figuras como asistente)
            </span>
          </v-timeline-item>
          <template v-for="(date, index) in Object.keys(eventsMap)">
            <v-timeline-item
              :key="`${date}_dot`"
              class="mb-4"
              hide-dot
              :right="index % 2 !== 0"
              :left="index % 2 === 0"
            >
              <span class="text-h6">{{ date }}</span>
            </v-timeline-item>
            <template v-for="event in eventsMap[date]">
              <v-timeline-item
                :key="event.id"
                :color="eventTypesMap[event.type].colour"
                :icon="eventTypesMap[event.type].icon"
                :icon-color="getFontColourFromBackground(eventTypesMap[event.type].colour)"
                fill-dot
                :right="index % 2 !== 0"
                :left="index % 2 === 0"
              >
                <v-card class="elevation-5">
                  <v-toolbar
                    :color="eventTypesMap[event.type].colour"
                    :dark="applyDarkVariant(eventTypesMap[event.type].colour)"
                    flat
                  >
                    <v-toolbar-title>{{ event.name }}</v-toolbar-title>
                  </v-toolbar>
                  <v-divider />
                  <v-card-text>
                    <EventRepresentation :item="event" />
                  </v-card-text>
                  <v-card-actions>
                    <v-btn text color="primary" @click="viewInCalendar(event)"> Ver en el calendario </v-btn>
                  </v-card-actions>
                </v-card>
              </v-timeline-item>
            </template>
          </template>
          <v-timeline-item fill-dot class="mb-5" color="secondary" large>
            <template #icon>
              <v-icon dark>mdi-dots-horizontal-circle-outline</v-icon>
            </template>
          </v-timeline-item>
        </v-timeline>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, onActivated } from "@vue/composition-api";
import { DateTime } from "luxon";
import { groupBy } from "lodash-es";

import CalendarEvent from "@/modules/calendar/models/event";

import EventService from "@/modules/calendar/services/event-service";

import EventRepresentation from "@/modules/calendar/components/EventRepresentation";

import { useMainStore } from "@/stores/main";

import { useEventTypes } from "@/modules/calendar/composables/event-types";
import { useLoading } from "@/composables/loading";
import { applyDarkVariant, getFontColourFromBackground } from "@/utils/colours";

export default {
  name: "TimelineView",
  metaInfo: {
    title: "Timeline",
  },
  components: {
    EventRepresentation,
  },
  setup(props, { root }) {
    // Store
    const store = useMainStore();

    // Composables
    const { isLoading, addTask, removeTask } = useLoading();
    const { eventTypesMap } = useEventTypes();

    // State
    const events = ref([]);

    // Computed
    const eventsMap = computed(() =>
      groupBy(events.value, (event) => {
        return event.luxonStart.setLocale(store.locale).toLocaleString(DateTime.DATE_HUGE);
      })
    );

    // Methods
    async function fetchTimeLine() {
      addTask("fetch-timeline");
      try {
        const response = await EventService.myTimeline();
        events.value = response.data.results.map((event) => {
          return new CalendarEvent(event);
        });
      } finally {
        removeTask("fetch-timeline");
      }
    }
    function viewInCalendar(event) {
      const date = DateTime.fromISO(event.start_datetime).toISODate();
      root.$router.push({ name: "calendar", params: { initialDate: date } });
    }

    // Lifecycle hooks
    onActivated(() => fetchTimeLine());

    return {
      // State
      events,
      // Computed
      eventTypesMap,
      eventsMap,
      // Methods
      isLoading,
      viewInCalendar,
      applyDarkVariant,
      getFontColourFromBackground,
    };
  },
};
</script>
