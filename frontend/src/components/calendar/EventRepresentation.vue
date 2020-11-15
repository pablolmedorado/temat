<template>
  <v-container>
    <template v-if="startDate === endDate">
      <v-row>
        <v-col>
          <v-chip>
            <v-icon left>mdi-calendar</v-icon>
            {{ dateLocaleString(item.luxonStart) }}
          </v-chip>
          <template v-if="!item.all_day && startTime !== endTime">
            &nbsp;
            <v-chip>
              <v-icon left>mdi-clock-outline</v-icon>
              {{ startTime }} - {{ endTime }}
            </v-chip>
          </template>
          <template v-else-if="!item.all_day && startTime === endTime">
            <v-chip>
              <v-icon left>mdi-clock-outline</v-icon>
              {{ startTime }}
            </v-chip>
          </template>
        </v-col>
      </v-row>
    </template>
    <template v-else>
      <template v-if="item.all_day">
        <v-row>
          <v-col>
            <v-chip>
              <v-icon left>mdi-calendar</v-icon>
              {{ dateLocaleString(item.luxonStart) }} - {{ dateLocaleString(item.luxonEnd) }}
            </v-chip>
          </v-col>
        </v-row>
      </template>
      <template v-else>
        <v-row>
          <v-col>
            <span class="time-label">Inicio:</span>
            <v-chip>
              <v-icon left>mdi-calendar</v-icon>
              {{ dateLocaleString(item.luxonStart) }}
            </v-chip>
            &nbsp;
            <v-chip>
              <v-icon left>mdi-clock-outline</v-icon>
              {{ startTime }}
            </v-chip>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <span class="time-label">Fin:</span>
            <v-chip>
              <v-icon left>mdi-calendar</v-icon>
              {{ dateLocaleString(item.luxonEnd) }}
            </v-chip>
            &nbsp;
            <v-chip>
              <v-icon left>mdi-clock-outline</v-icon>
              {{ endTime }}
            </v-chip>
          </v-col>
        </v-row>
      </template>
    </template>
    <v-row v-if="item.location">
      <v-col>
        <v-chip :href="`https://www.google.com/maps/search/${item.location}/`" target="_blank">
          <v-icon left color="red">mdi-map-marker</v-icon>
          {{ item.location }}
        </v-chip>
      </v-col>
    </v-row>
    <v-row v-if="item.details">
      <v-col>
        <div class="text-subtitle-1 font-weight-medium">Detalles:</div>
        <div>{{ item.details }}</div>
      </v-col>
    </v-row>
    <v-row v-if="item.attendees.length">
      <v-col>
        <div class="text-subtitle-1 font-weight-medium">Usuarios invitados:</div>
        <v-chip-group column>
          <UserPill v-for="(attendee, index) in item.attendees" :key="`attendee-${index}`" :user="attendee" />
        </v-chip-group>
      </v-col>
    </v-row>
    <v-row v-if="item.groups.length">
      <v-col>
        <div class="text-subtitle-1 font-weight-medium">Grupos invitados:</div>
        <v-chip-group column>
          <GroupPill v-for="(group, index) in item.groups" :key="`group-${index}`" :group="group" />
        </v-chip-group>
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <div class="text-subtitle-1 font-weight-medium">Tags:</div>
        <div class="v-chip-group v-chip-group--column">
          <v-chip
            v-if="Object.keys(eventTypesMap).length"
            class="elevation-1"
            :color="eventTypesMap[item.type].colour"
            :dark="applyDarkVariant(eventTypesMap[item.type].colour)"
            label
          >
            <v-icon left>{{ eventTypesMap[item.type].icon }}</v-icon>
            {{ eventTypesMap[item.type].name }}
          </v-chip>
          <v-chip
            v-if="Object.keys(eventVisibilityTypesMap).length"
            class="elevation-1"
            :color="eventVisibilityTypesMap[item.visibility].colour"
            label
            dark
          >
            <v-icon left>{{ eventVisibilityTypesMap[item.visibility].icon }}</v-icon>
            {{ eventVisibilityTypesMap[item.visibility].label }}
          </v-chip>
          <AuthorshipTag v-if="item.creation_user || item.modification_user" :event="item" color="teal" dark label />
          <v-chip v-for="tag in item.tags" :key="tag" class="elevation-1" color="info" label>
            <v-icon left>mdi-label</v-icon>
            {{ tag }}
          </v-chip>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { DateTime } from "luxon";

import AuthorshipTag from "@/components/calendar/AuthorshipTag";

import { applyDarkVariant } from "@/utils/colours";
import { getReadableDuration } from "@/utils/dates";

export default {
  name: "EventRepresentation",
  components: { AuthorshipTag },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  computed: {
    ...mapState(["locale"]),
    ...mapGetters("calendar", ["eventTypesMap", "eventVisibilityTypesMap"]),
    ...mapGetters("users", ["usersMap"]),
    startDate() {
      return this.item.luxonStart.toISODate();
    },
    startTime() {
      return this.item.luxonStart.toFormat("HH:mm");
    },
    endDate() {
      return this.item.luxonEnd.toISODate();
    },
    endTime() {
      return this.item.luxonEnd.toFormat("HH:mm");
    },
    readableDuration() {
      return getReadableDuration(this.item.luxonEnd.diff(this.item.luxonStart).toObject());
    },
  },
  created() {
    if (!Object.keys(this.eventTypesMap).length) {
      this.fetchEventTypes();
    }
  },
  methods: {
    ...mapActions("calendar", ["fetchEventTypes"]),
    applyDarkVariant,
    dateLocaleString(dateTime) {
      return dateTime.setLocale(this.locale).toLocaleString(DateTime.DATE_HUGE);
    },
  },
};
</script>

<style scoped>
.time-label {
  display: inline-block;
  min-width: 60px;
}
</style>
