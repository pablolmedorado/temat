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
      <template v-if="!eventTypesMap[item.type].system">
        <v-divider vertical inset />
        <v-btn v-if="isEditable" icon @click="onEdit(item)">
          <v-icon>mdi-pencil</v-icon>
        </v-btn>
        <v-btn icon @click="onEdit(itemForCopy)">
          <v-icon>mdi-content-copy</v-icon>
        </v-btn>
        <v-btn v-if="isEditable" icon @click.stop="onDelete(item)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-toolbar>
    <v-divider />

    <EventRepresentation :item="item" />

    <v-divider />
    <v-card-actions>
      <v-spacer />
      <v-btn text color="primary" @click="$emit('close:dialog')">Volver</v-btn>
    </v-card-actions>

    <FormDialog ref="formDialog" verbose-name="evento" :form-component="formComponent" @submit="onFormSubmit" />

    <DeletionConfirmationDialog ref="deleteDialog" @confirm="onDeleteConfirm" />
  </v-card>
</template>

<script>
import EventEditionMixin from "@/mixins/calendar/event-edition-mixin";

import { applyDarkVariant } from "@/utils/colours";

export default {
  name: "EventCard",
  mixins: [EventEditionMixin],
  inheritAttrs: false,
  props: {
    item: {
      type: Object,
      required: true,
    },
  },
  methods: {
    applyDarkVariant,
    onFormSubmit(newItem) {
      this.$emit("update:event", newItem);
      this.$emit("close:dialog");
    },
    async onDeleteConfirm() {
      await this.service.delete(this.item.id);
      this.$emit("delete:event", this.item);
      this.$emit("close:dialog");
    },
  },
};
</script>
