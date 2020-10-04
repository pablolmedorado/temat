<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-key="notification"
          verbose-name="Notificación"
          verbose-name-plural="Notificaciones"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :service="service"
          custom-headers
          read-only
          selectable-rows
        >
          <template #toolbar="{ selectedItems }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :disabled="loading || !Boolean(selectedItems.length)"
                  v-bind="attrs"
                  @click="performBulkAction('markAllAsRead', selectedItems)"
                  v-on="on"
                >
                  <v-icon>mdi-email-open</v-icon>
                </v-btn>
              </template>
              <span>
                Marcar como leído
              </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :disabled="loading || !Boolean(selectedItems.length)"
                  v-bind="attrs"
                  @click="performBulkAction('markAllAsUnread', selectedItems)"
                  v-on="on"
                >
                  <v-icon>mdi-email-mark-as-unread</v-icon>
                </v-btn>
              </template>
              <span>
                Marcar como no leído
              </span>
            </v-tooltip>
            <v-btn icon :disabled="loading || !Boolean(selectedItems.length)" @click="openDeleteDialog(selectedItems)">
              <v-icon>mdi-delete</v-icon>
            </v-btn>
            <v-divider vertical inset />
          </template>

          <template #item.timestamp="{ value }">
            {{ value | datetime }}
          </template>
          <template #item.target_content_type="{ value }">
            <v-tooltip v-if="value" bottom>
              <template #activator="{ on, attrs }">
                <v-icon v-bind="attrs" v-on="on">{{ notificationTargetMap[value].icon }}</v-icon>
              </template>
              <span>
                {{ notificationTargetMap[value].text }}
              </span>
            </v-tooltip>
          </template>
          <template #item.level="{ value }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-icon :color="value" v-bind="attrs" v-on="on">{{ levelIcons[value] }}</v-icon>
              </template>
              <span>
                {{ value }}
              </span>
            </v-tooltip>
          </template>
          <template #item.actor="{ value }">
            <UserPill :user="value"></UserPill>
          </template>
          <template #item.target="{ value }">
            {{ value ? value.representation : "" }}
          </template>
          <template #item.unread="{ value }">
            <v-simple-checkbox :value="!value" disabled></v-simple-checkbox>
          </template>
          <template #item.table_actions="{ item }">
            <v-btn
              v-if="item.target"
              icon
              :to="{
                ...notificationTargetMap[item.target_content_type].route,
                params: { id: item.target.id }
              }"
            >
              <v-icon>mdi-open-in-app</v-icon>
            </v-btn>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <DeletionConfirmationDialog ref="deleteDialog" @confirm="performBulkAction('bulkDelete', $event)" />
  </v-container>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

import NotificationService from "@/services/notifications/notification-service";

import NotificationFilters from "@/components/notifications/NotificationFilters";

import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "Notifications",
  filters: {
    datetime: isoDateTimeToLocaleString
  },
  data() {
    return {
      tableHeaders: [
        { text: "Fecha", align: "start", sortable: true, value: "timestamp", fixed: true },
        {
          text: "Tipo",
          align: "start",
          sortable: true,
          value: "target_content_type",
          sortingField: "target_content_type__model",
          default: true
        },
        { text: "Nivel", align: "start", sortable: true, value: "level", default: true },
        { text: "Quién", align: "start", sortable: false, value: "actor", default: true },
        { text: "Qué", align: "start", sortable: true, value: "verb", fixed: true },
        {
          text: "Registro",
          align: "start",
          sortable: false,
          value: "target",
          fixed: true
        },
        { text: "Leída", align: "start", sortable: true, value: "unread", fixed: true },
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true }
      ],
      tableOptions: {
        sortBy: ["unread", "timestamp"],
        sortDesc: [true, true],
        multiSort: true
      },
      service: NotificationService,
      filterComponent: NotificationFilters,
      levelIcons: {
        success: "mdi-check",
        info: "mdi-information",
        warning: "mdi-exclamation",
        error: "mdi-alert"
      }
    };
  },
  computed: {
    ...mapGetters(["loading"]),
    ...mapGetters("notifications", ["notificationTargetMap"])
  },
  methods: {
    ...mapActions("notifications", ["getUnreadCount"]),
    async performBulkAction(actionFunctionName, selectedItems) {
      const params = { id__in: selectedItems.map(item => item.id).join(",") };
      await this.service[actionFunctionName](params);
      this.postBulkAction();
    },
    postBulkAction() {
      this.$refs.itemIndex.fetchTableItems();
      this.getUnreadCount();
    },
    openDeleteDialog(selectedItems) {
      this.$refs.deleteDialog.open(selectedItems);
    }
  }
};
</script>
