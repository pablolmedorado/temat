<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          custom-headers
          selectable-rows
        >
          <template #toolbar="{ selectedItems }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :disabled="isLoading || !Boolean(selectedItems.length)"
                  :loading="isTaskLoading('bulk-action', 'markAllAsRead')"
                  v-bind="attrs"
                  @click="performBulkAction('markAllAsRead', selectedItems)"
                  v-on="on"
                >
                  <v-icon>mdi-email-open</v-icon>
                </v-btn>
              </template>
              <span> Marcar como leído </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :disabled="isLoading || !Boolean(selectedItems.length)"
                  :loading="isTaskLoading('bulk-action', 'markAllAsUnread')"
                  v-bind="attrs"
                  @click="performBulkAction('markAllAsUnread', selectedItems)"
                  v-on="on"
                >
                  <v-icon>mdi-email-mark-as-unread</v-icon>
                </v-btn>
              </template>
              <span> Marcar como no leído </span>
            </v-tooltip>
            <v-btn
              icon
              :disabled="isLoading || !Boolean(selectedItems.length)"
              :loading="isTaskLoading('bulk-action', 'bulkDelete')"
              @click.stop="openDeleteDialog(selectedItems)"
            >
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
            <UserPill :user="value" />
          </template>
          <template #item.target="{ value }">
            {{ value ? value.representation : "" }}
          </template>
          <template #item.unread="{ value }">
            <v-simple-checkbox :value="!value" disabled />
          </template>
          <template #item.table_actions="{ item }">
            <v-btn
              v-if="item.target"
              icon
              :to="{
                ...notificationTargetMap[item.target_content_type].route,
                params: { id: item.target.id },
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

import Notification from "@/models/common/notification";

import NotificationFilters from "@/components/notifications/NotificationFilters";

import useLoading from "@/composables/useLoading";
import { getServiceByBasename } from "@/services";
import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "Notifications",
  metaInfo: {
    title: "Notificaciones",
  },
  filters: {
    datetime: isoDateTimeToLocaleString,
  },
  setup() {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });
    return {
      isLoading,
      isTaskLoading,
      addTask,
      removeTask,
    };
  },
  data() {
    return {
      modelClass: Notification,
      service: getServiceByBasename(Notification.serviceBasename),
      tableHeaders: [
        { text: "Fecha", align: "start", sortable: true, value: "timestamp", fixed: true },
        {
          text: "Tipo",
          align: "start",
          sortable: true,
          value: "target_content_type",
          sortingField: "target_content_type__model",
          default: true,
        },
        { text: "Nivel", align: "start", sortable: true, value: "level", default: true },
        { text: "Quién", align: "start", sortable: false, value: "actor", default: true },
        { text: "Qué", align: "start", sortable: true, value: "verb", fixed: true },
        {
          text: "Registro",
          align: "start",
          sortable: false,
          value: "target",
          fixed: true,
        },
        { text: "Leída", align: "start", sortable: true, value: "unread", fixed: true },
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
      ],
      tableOptions: {
        sortBy: ["unread", "timestamp"],
        sortDesc: [true, true],
        multiSort: true,
      },
      filterComponent: NotificationFilters,
      levelIcons: {
        success: "mdi-check",
        info: "mdi-information",
        warning: "mdi-exclamation",
        error: "mdi-alert",
      },
    };
  },
  computed: {
    ...mapGetters("notifications", ["notificationTargetMap"]),
  },
  methods: {
    ...mapActions("notifications", ["getUnreadCount"]),
    async performBulkAction(actionFunctionName, selectedItems) {
      this.addTask("bulk-action", actionFunctionName);
      try {
        const params = { id__in: selectedItems.map((item) => item.id).join(",") };
        await this.service[actionFunctionName](params);
        this.$refs.itemIndex.fetchTableItems();
        this.getUnreadCount();
      } finally {
        this.removeTask("bulk-action", actionFunctionName);
      }
    },
    openDeleteDialog(selectedItems) {
      this.$refs.deleteDialog.open(selectedItems);
    },
  },
};
</script>
