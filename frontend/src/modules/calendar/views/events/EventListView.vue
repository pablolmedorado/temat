<template>
  <v-container fluid>
    <v-breadcrumbs :items="breadcrumbs" />
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :system-filters="systemFilters"
          :quick-filters="quickFilters"
          default-quick-filter="next-events"
          custom-headers
        >
          <template #item.type="{ value }">
            <v-tooltip v-if="value" bottom>
              <template #activator="{ on, attrs }">
                <v-icon v-bind="attrs" v-on="on">{{ eventTypesMap[value].icon }}</v-icon>
              </template>
              <span>
                {{ eventTypesMap[value].name }}
              </span>
            </v-tooltip>
          </template>
          <template #item.start_datetime="{ item }">
            <template v-if="item.all_day">
              {{ item.start_datetime | date }}
            </template>
            <template v-else>
              {{ item.start_datetime | datetime(datetimeFormat) }}
            </template>
          </template>
          <template #item.duration="{ item }">
            <template v-if="!item.all_day">
              {{ calculateDuration(item) }}
            </template>
          </template>
          <template #item.visibility="{ value }">
            <v-tooltip v-if="value && Object.keys(eventVisibilityTypesMap).length" bottom>
              <template #activator="{ on, attrs }">
                <v-icon v-bind="attrs" v-on="on">{{ eventVisibilityTypesMap[value].icon }}</v-icon>
              </template>
              <span>
                {{ eventVisibilityTypesMap[value].label }}
              </span>
            </v-tooltip>
          </template>
          <template #item.tags="{ value }">
            <TagLabels v-if="value" :tags="value" small @click:tag="setTagFilter" />
          </template>
          <template #item.table_actions="{ item }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn icon :to="{ name: 'event', params: { id: item.id } }" v-bind="attrs" v-on="on">
                  <v-icon>mdi-open-in-app</v-icon>
                </v-btn>
              </template>
              <span> Ver detalle </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :to="{ name: 'calendar', params: { initialDate: extractIsoDate(item.start_datetime) } }"
                  exact
                >
                  <v-icon v-bind="attrs" v-on="on">mdi-calendar-search</v-icon>
                </v-btn>
              </template>
              <span> Ver en el calendario </span>
            </v-tooltip>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { computed, nextTick, toRefs } from "@vue/composition-api";
import { DateTime } from "luxon";

import CalendarEvent from "@/modules/calendar/models/event";

import { useEventStore } from "@/modules/calendar/stores/events";

import EventFilters from "@/modules/calendar/components/filters/EventFilters";

import { useEventTypes } from "@/modules/calendar/composables/event-types";

import { getReadableDuration, isoDateToLocaleString, isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "EventListView",
  metaInfo: {
    title: "Eventos",
  },
  filters: {
    date: isoDateToLocaleString,
    datetime: isoDateTimeToLocaleString,
  },
  setup(props, { refs }) {
    // Store
    const eventStore = useEventStore();

    // Composables
    const { eventTypesMap } = useEventTypes();

    // State
    const modelClass = CalendarEvent;
    const tableHeaders = [
      { text: "Nombre", align: "start", sortable: true, value: "name", fixed: true },
      { text: "Tipo", align: "start", sortable: true, sortingField: "type__name", value: "type", default: true },
      {
        text: "Fecha de inicio",
        align: "start",
        sortable: true,
        value: "start_datetime",
        fields: ["start_datetime", "all_day"],
        default: true,
      },
      {
        text: "Duración",
        align: "start",
        sortable: false,
        value: "duration",
        fields: ["start_datetime", "end_datetime"],
        default: true,
      },
      { text: "Visibilidad", align: "start", sortable: true, value: "visibility", default: true },
      {
        text: "Tags",
        align: "start",
        sortable: false,
        value: "tags",
        fields: ["tags.name", "tags.colour", "tags.icon"],
      },
      { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
    ];
    const tableOptions = {
      sortBy: ["start_datetime"],
      sortDesc: [true],
      mustSort: true,
    };
    const filterComponent = EventFilters;
    const systemFilters = { type__system_slug__isnull: true };
    const datetimeFormat = DateTime.DATETIME_MED_WITH_WEEKDAY;
    const breadcrumbs = [
      { text: "Calendario", to: { name: "calendar" }, exact: true },
      { text: "Eventos", disabled: true },
    ];

    // Computed
    const { eventVisibilityTypesMap } = toRefs(eventStore);
    const quickFilters = computed(() => [
      {
        key: "next-events",
        label: "Próximos eventos",
        filters: { start_datetime__date__gte: DateTime.local().toISODate() },
      },
    ]);

    // Methods
    function calculateDuration(item) {
      const start = DateTime.fromISO(item.start_datetime);
      const end = DateTime.fromISO(item.end_datetime);
      return getReadableDuration(end.diff(start).toObject());
    }
    function extractIsoDate(datetime) {
      return DateTime.fromISO(datetime).toISODate();
    }
    function setTagFilter(tag) {
      refs.itemIndex.addFilter({ tags__name__in: tag });
      nextTick(() => {
        refs.itemIndex.fetchTableItems();
      });
    }

    return {
      // State
      modelClass,
      tableHeaders,
      tableOptions,
      filterComponent,
      systemFilters,
      datetimeFormat,
      breadcrumbs,
      // Computed
      eventTypesMap,
      eventVisibilityTypesMap,
      quickFilters,
      // Methods
      calculateDuration,
      extractIsoDate,
      setTagFilter,
    };
  },
};
</script>
