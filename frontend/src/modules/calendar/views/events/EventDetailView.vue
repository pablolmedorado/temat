<template>
  <v-container v-if="item && Object.keys(eventTypesMap).length" fluid>
    <v-breadcrumbs :items="breadcrumbs" />
    <v-card>
      <v-toolbar flat>
        <v-toolbar-title class="text-h6">{{ item.name }}</v-toolbar-title>
        <v-spacer />
        <v-btn icon :to="{ name: 'calendar', params: { initialDate: item.luxonStart.toISODate() } }" exact>
          <v-icon>mdi-calendar-search</v-icon>
        </v-btn>
        <v-menu bottom offset-y>
          <template #activator="{ on, attrs }">
            <v-btn icon v-bind="attrs" v-on="on"><v-icon>mdi-export</v-icon></v-btn>
          </template>
          <v-list>
            <v-list-item :href="googleCalendarUrl" target="_blank">
              <v-list-item-icon>
                <v-icon>mdi-google</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Google Calendar</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
            <v-list-item :href="buildIcalUrl(item)">
              <v-list-item-icon>
                <v-icon>mdi-microsoft-outlook</v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <v-list-item-title>Microsoft Outlook (.ics)</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-menu>
      </v-toolbar>
      <v-card-text>
        <EventRepresentation :item="item" />
      </v-card-text>
    </v-card>

    <v-speed-dial
      v-if="canChange"
      v-model="showSpeedDial"
      fixed
      bottom
      right
      direction="top"
      open-on-hover
      transition="slide-y-reverse-transition"
    >
      <template #activator>
        <v-btn fab dark color="secondary" @click="onEdit(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
      </template>
      <v-btn v-if="canCopy" fab dark small color="secondary" @click="onCopy(item)">
        <v-icon>mdi-content-copy</v-icon>
      </v-btn>
      <v-btn v-if="canDelete" fab dark small color="red" @click.stop="onDelete(item)">
        <v-icon>mdi-delete</v-icon>
      </v-btn>
    </v-speed-dial>

    <FormDialog ref="formDialog" verbose-name="evento" :form-component="formComponent" @submit="onFormSubmit" />

    <DeletionConfirmationDialog ref="deleteDialog" @confirm="onDeleteConfirm" />
  </v-container>
</template>

<script>
import { ref, computed } from "@vue/composition-api";
import { cloneDeep, get } from "lodash-es";

import CalendarEvent from "@/modules/calendar/models/event";

import EventService from "@/modules/calendar/services/event-service";

import EventForm from "@/modules/calendar/components/forms/EventForm";
import EventRepresentation from "@/modules/calendar/components/EventRepresentation";

import { useMainStore } from "@/stores/main";

import { useEventTypes } from "@/modules/calendar/composables/event-types";
import { handleError } from "@/utils/error-handlers";
import { userHasPermission } from "@/utils/permissions";
import { truncate } from "@/utils/text";
import { buildGoogleCalendarUrl } from "@/modules/calendar/utils";

export default {
  name: "EventDetailView",
  metaInfo: {
    title: "Evento",
  },
  components: { EventRepresentation },
  async beforeRouteEnter(to, from, next) {
    try {
      const response = await EventService.retrieve(to.params.id, { expand: "tags" });
      next((vm) => {
        vm.item = new CalendarEvent(response.data);
      });
    } catch (error) {
      handleError(error);
      if (from.name === null) {
        next({ name: "events" });
      }
    }
  },
  async beforeRouteUpdate(to, from, next) {
    this.item = null;
    try {
      await this.fetchItem(to.params.id);
      next();
    } catch (error) {
      handleError(error);
      next({ name: "events" });
    }
  },
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  setup(props, { refs, root }) {
    // Store
    const mainStore = useMainStore();

    // Composables
    const { eventTypesMap } = useEventTypes();

    // State
    const formComponent = EventForm;
    const item = ref(null);
    const showSpeedDial = ref(false);

    // Computed
    const canChange = computed(() => {
      return (
        mainStore.currentUser.id === item.value.creation_user || userHasPermission(CalendarEvent.CHANGE_PERMISSION)
      );
    });
    const canCopy = computed(() => {
      return mainStore.currentUser.id === item.value.creation_user || userHasPermission(CalendarEvent.ADD_PERMISSION);
    });
    const canDelete = computed(() => {
      return (
        mainStore.currentUser.id === item.value.creation_user || userHasPermission(CalendarEvent.DELETE_PERMISSION)
      );
    });
    const breadcrumbs = computed(() => {
      const text = get(item.value, "name", "Evento");
      return [
        { text: "Calendario", to: { name: "calendar" }, exact: true },
        { text: "Eventos", to: { name: "events" }, exact: true },
        { text: truncate(text, 50), disabled: true },
      ];
    });
    const googleCalendarUrl = computed(() => buildGoogleCalendarUrl(item.value));

    // Methods
    async function fetchItem(id) {
      const response = await EventService.retrieve(id, { expand: "tags" });
      item.value = new CalendarEvent(response.data);
    }
    function onEdit(itemToEdit) {
      refs.formDialog.open(itemToEdit);
    }
    function onCopy(itemToCopy) {
      const copy = cloneDeep(itemToCopy);
      delete copy.id;
      refs.formDialog.open(copy);
    }
    function onFormSubmit(newItem) {
      item.value = new CalendarEvent(newItem);
    }
    function onDelete(itemToDelete) {
      refs.deleteDialog.open(itemToDelete);
    }
    async function onDeleteConfirm() {
      await EventService.delete(item.value.id);
      mainStore.showSnackbar({ color: "success", message: "Evento eliminado correctamente" });
      root.$router.push({ name: "events" });
    }
    function buildIcalUrl({ id }) {
      return `${Urls["calendar:event-ical"]()}?id=${id}&page_size=1`;
    }

    return {
      // State
      formComponent,
      item,
      showSpeedDial,
      // Computed
      eventTypesMap,
      canChange,
      canCopy,
      canDelete,
      breadcrumbs,
      googleCalendarUrl,
      // Methods
      fetchItem,
      onEdit,
      onCopy,
      onFormSubmit,
      onDelete,
      onDeleteConfirm,
      buildIcalUrl,
    };
  },
};
</script>
