<template>
  <div>
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
        <div class="text-pre-wrap">{{ item.details }}</div>
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
          <EventAuthorshipTag
            v-if="item.creation_user || item.modification_user"
            :event="item"
            color="teal"
            dark
            label
          />
          <v-chip
            v-for="tag in item.tags"
            :key="camelCase(tag.name)"
            class="elevation-1"
            :color="tag.colour"
            :dark="applyDarkVariant(tag.colour)"
            label
          >
            <v-icon left>{{ tag.icon }}</v-icon>
            {{ tag.name }}
          </v-chip>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { computed, toRefs } from "@vue/composition-api";
import { camelCase } from "lodash-es";
import { DateTime } from "luxon";

import { useEventStore } from "@/modules/calendar/stores/events";
import { useMainStore } from "@/stores/main";

import EventAuthorshipTag from "@/modules/calendar/components/EventAuthorshipTag";

import { useEventTypes } from "@/modules/calendar/composables/event-types";

import { applyDarkVariant } from "@/utils/colours";
import { getReadableDuration } from "@/utils/dates";

export default {
  name: "EventRepresentation",
  components: { EventAuthorshipTag },
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    // Store
    const mainStore = useMainStore();
    const eventStore = useEventStore();

    // Composables
    const { eventTypesMap } = useEventTypes();

    // Computed
    const { eventVisibilityTypesMap } = toRefs(eventStore);
    const startDate = computed(() => props.item.luxonStart.toISODate());
    const startTime = computed(() => props.item.luxonStart.toFormat("HH:mm"));
    const endDate = computed(() => props.item.luxonEnd.toISODate());
    const endTime = computed(() => props.item.luxonEnd.toFormat("HH:mm"));
    const readableDuration = computed(() =>
      getReadableDuration(props.item.luxonEnd.diff(props.item.luxonStart).toObject())
    );

    // Methods
    function dateLocaleString(dateTime) {
      return dateTime.setLocale(mainStore.locale).toLocaleString(DateTime.DATE_HUGE);
    }

    return {
      // Computed
      eventTypesMap,
      eventVisibilityTypesMap,
      startDate,
      startTime,
      endDate,
      endTime,
      readableDuration,
      // Methods
      camelCase,
      applyDarkVariant,
      dateLocaleString,
    };
  },
};
</script>

<style scoped>
.time-label {
  display: inline-block;
  min-width: 60px;
}
.text-pre-wrap {
  white-space: pre-wrap;
}
</style>
