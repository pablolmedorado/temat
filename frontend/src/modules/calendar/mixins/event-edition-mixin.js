import { mapActions, mapGetters, mapState } from "vuex";
import { cloneDeep } from "lodash";

import CalendarEvent from "@/modules/calendar/models/event";

import EventService from "@/modules/calendar/services/event-service";

import EventForm from "@/modules/calendar/components/forms/EventForm";
import EventRepresentation from "@/modules/calendar/components/EventRepresentation";

import { userHasPermission } from "@/utils/permissions";

export default {
  components: { EventRepresentation },
  data() {
    return {
      service: EventService,
      formComponent: EventForm,
    };
  },
  computed: {
    ...mapState(["loggedUser", "tz"]),
    ...mapGetters("calendar", ["eventTypesMap"]),
    canChange() {
      return this.loggedUser.id === this.item.creation_user || userHasPermission(CalendarEvent.CHANGE_PERMISSION);
    },
    canCopy() {
      return this.loggedUser.id === this.item.creation_user || userHasPermission(CalendarEvent.ADD_PERMISSION);
    },
    canDelete() {
      return this.loggedUser.id === this.item.creation_user || userHasPermission(CalendarEvent.DELETE_PERMISSION);
    },
    itemForCopy() {
      const copy = cloneDeep(this.item);
      delete copy.id;
      return copy;
    },
    googleCalendarUrl() {
      const baseUrl = `https://calendar.google.com/calendar/render?action=TEMPLATE&ctz=${this.tz}`;

      const eventType = `[${this.eventTypesMap[this.item.type].name}] `;

      let dateFormat = "yyyyMMdd'T'HHmm'00'";
      let auxLuxonEnd = this.item.luxonEnd;
      if (this.item.all_day) {
        dateFormat = "yyyyMMdd";
        auxLuxonEnd = auxLuxonEnd.plus({ days: 1 });
      }
      const startDateStr = this.item.luxonStart.toFormat(dateFormat);
      const endDateStr = auxLuxonEnd.toFormat(dateFormat);
      const dates = `${startDateStr}/${endDateStr}`;

      return `${baseUrl}&text=${eventType}${this.item.name}&dates=${dates}&details=${this.item.details}&location=${this.item.location}`;
    },
  },
  created() {
    if (!Object.keys(this.eventTypesMap).length) {
      this.fetchEventTypes();
    }
  },
  methods: {
    ...mapActions("calendar", ["fetchEventTypes"]),
    onEdit(item) {
      this.$refs.formDialog.open(item);
    },
    onDelete(item) {
      this.$refs.deleteDialog.open(item);
    },
    buildIcalUrl(item) {
      return `${Urls["calendar:event-ical"]()}?id=${item.id}&page_size=1`;
    },
  },
};
