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
      <v-btn v-if="canCopy" fab dark small color="secondary" @click="onEdit(itemForCopy)">
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
import { mapActions } from "vuex";
import { get } from "lodash";

import CalendarEvent from "@/models/calendar/event";

import EventEditionMixin from "@/mixins/calendar/event-edition-mixin";

import EventService from "@/services/calendar/event-service";

import { handleError } from "@/utils/error-handlers";
import { truncate } from "@/filters";

export default {
  name: "EventDetail",
  metaInfo: {
    title: "Evento",
  },
  mixins: [EventEditionMixin],
  async beforeRouteEnter(to, from, next) {
    try {
      const response = await EventService.retrieve(to.params.id);
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
  data() {
    return {
      item: null,
      showSpeedDial: false,
    };
  },
  computed: {
    breadcrumbs() {
      const text = get(this.item, "name", "Evento");
      return [
        { text: "Calendario", to: { name: "calendar" }, exact: true },
        { text: "Eventos", to: { name: "events" }, exact: true },
        { text: truncate(text, 50), disabled: true },
      ];
    },
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    async fetchItem(id) {
      const response = await this.service.retrieve(id);
      this.item = new CalendarEvent(response.data);
    },
    onFormSubmit(newItem) {
      this.item = new CalendarEvent(newItem);
    },
    async onDeleteConfirm() {
      await this.service.delete(this.item.id);
      this.showSnackbar({ color: "success", message: "Evento eliminado correctamente" });
      this.$router.push({ name: "events" });
    },
  },
};
</script>
