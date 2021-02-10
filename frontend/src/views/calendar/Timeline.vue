<template>
  <v-container fluid>
    <v-row v-show="!loading">
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
                  <EventRepresentation :item="event" />
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
import { mapActions, mapGetters, mapState } from "vuex";
import { DateTime } from "luxon";
import { groupBy } from "lodash";

import CalendarEvent from "@/models/event";

import EventService from "@/services/calendar/event-service";

import EventRepresentation from "@/components/calendar/EventRepresentation";

import { applyDarkVariant, getFontColourFromBackground } from "@/utils/colours";

export default {
  name: "Timeline",
  metaInfo: {
    title: "Timeline",
  },
  components: {
    EventRepresentation,
  },
  data() {
    return {
      events: [],
    };
  },
  computed: {
    ...mapState(["locale"]),
    ...mapGetters(["loading"]),
    ...mapGetters("calendar", ["eventTypesMap", "eventVisibilityTypesMap"]),
    eventsMap() {
      return groupBy(this.events, (event) => {
        return event.luxonStart.setLocale(this.locale).toLocaleString(DateTime.DATE_HUGE);
      });
    },
  },
  created() {
    if (!Object.keys(this.eventTypesMap).length) {
      this.fetchEventTypes();
    }
  },
  activated() {
    this.getTimeLine();
  },
  methods: {
    ...mapActions("calendar", ["fetchEventTypes"]),
    applyDarkVariant,
    getFontColourFromBackground,
    async getTimeLine() {
      const response = await EventService.myTimeline();
      this.events = response.data.results.map((event) => {
        return new CalendarEvent(event);
      });
    },
    viewInCalendar(event) {
      const date = DateTime.fromISO(event.start_datetime).toISODate();
      this.$router.push({ name: "calendar", params: { initialDate: date } });
    },
  },
};
</script>
