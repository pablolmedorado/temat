<template>
  <v-card v-if="Object.keys(eventTypesMap).length" v-bind="$attrs">
    <v-toolbar :color="eventTypesMap[item.type].colour" :dark="applyDarkVariant(eventTypesMap[item.type].colour)" flat>
      <v-toolbar-title>{{ item.name }}</v-toolbar-title>
      <v-spacer />
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
      <template v-if="!eventTypesMap[item.type].system_slug">
        <v-divider vertical inset />
        <v-btn v-if="canChange" icon @click="onEdit(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="onCopy(item)">
          <v-icon>mdi-content-copy</v-icon>
        </v-btn>
        <v-btn v-if="canDelete" icon @click.stop="onDelete(item)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-toolbar>
    <v-divider />

    <v-card-text>
      <EventRepresentation :item="item" />
    </v-card-text>

    <v-divider />
    <v-card-actions>
      <v-spacer />
      <v-btn text @click="$emit('close:dialog')">Volver</v-btn>
    </v-card-actions>

    <FormDialog ref="formDialog" verbose-name="evento" :form-component="formComponent" @submit="onFormSubmit" />

    <DeletionConfirmationDialog ref="deleteDialog" @confirm="onDeleteConfirm" />
  </v-card>
</template>

<script>
import { computed } from "@vue/composition-api";
import { cloneDeep } from "lodash-es";

import CalendarEvent from "@/modules/calendar/models/event";

import EventService from "@/modules/calendar/services/event-service";

import EventForm from "@/modules/calendar/components/forms/EventForm";
import EventRepresentation from "@/modules/calendar/components/EventRepresentation";

import { useMainStore } from "@/stores/main";

import useEventTypes from "@/modules/calendar/composables/useEventTypes";
import { userHasPermission } from "@/utils/permissions";
import { buildGoogleCalendarUrl } from "@/modules/calendar/utils";
import { applyDarkVariant } from "@/utils/colours";

export default {
  name: "EventCard",
  components: { EventRepresentation },
  inheritAttrs: false,
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  setup(props, { emit, refs }) {
    // Store
    const mainStore = useMainStore();

    // Composables
    const { eventTypesMap } = useEventTypes();

    // State
    const formComponent = EventForm;

    // Computed
    const canChange = computed(
      () => mainStore.currentUser.id === props.item.creation_user || userHasPermission(CalendarEvent.CHANGE_PERMISSION)
    );
    const canCopy = computed(
      () => mainStore.currentUser.id === props.item.creation_user || userHasPermission(CalendarEvent.ADD_PERMISSION)
    );
    const canDelete = computed(
      () => mainStore.currentUser.id === props.item.creation_user || userHasPermission(CalendarEvent.DELETE_PERMISSION)
    );
    const googleCalendarUrl = computed(() => buildGoogleCalendarUrl(props.item));

    // Methods
    function onEdit(itemToEdit) {
      refs.formDialog.open(itemToEdit);
    }
    function onCopy(itemToCopy) {
      const copy = cloneDeep(itemToCopy);
      delete copy.id;
      refs.formDialog.open(copy);
    }
    function onFormSubmit(newItem) {
      emit("update:event", newItem);
      emit("close:dialog");
    }
    function onDelete(itemToDelete) {
      refs.deleteDialog.open(itemToDelete);
    }
    async function onDeleteConfirm() {
      await EventService.delete(props.item.id);
      emit("delete:event", props.item);
      emit("close:dialog");
    }
    function buildIcalUrl({ id }) {
      return `${Urls["calendar:event-ical"]()}?id=${id}&page_size=1`;
    }

    return {
      // State
      formComponent,
      // Computed
      eventTypesMap,
      canChange,
      canCopy,
      canDelete,
      googleCalendarUrl,
      // Methods
      applyDarkVariant,
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
