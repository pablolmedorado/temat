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
                  <v-badge :value="selectedItems.length" :content="`${selectedItems.length}`" color="secondary" overlap>
                    <v-icon>mdi-email-open</v-icon>
                  </v-badge>
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
                  <v-badge :value="selectedItems.length" :content="`${selectedItems.length}`" color="secondary" overlap>
                    <v-icon>mdi-email-mark-as-unread</v-icon>
                  </v-badge>
                </v-btn>
              </template>
              <span> Marcar como no leído </span>
            </v-tooltip>
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <v-btn
                  icon
                  :disabled="isLoading || !Boolean(selectedItems.length)"
                  :loading="isTaskLoading('bulk-action', 'bulkDelete')"
                  v-bind="attrs"
                  @click.stop="openDeleteDialog(selectedItems)"
                  v-on="on"
                >
                  <v-badge :value="selectedItems.length" :content="`${selectedItems.length}`" color="error" overlap>
                    <v-icon>mdi-delete</v-icon>
                  </v-badge>
                </v-btn>
              </template>
              <span> Eliminar </span>
            </v-tooltip>
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
import { toRefs } from "@vue/composition-api";

import Notification from "@/modules/notifications/models/notification";

import NotificationFilters from "@/modules/notifications/components/filters/NotificationFilters";

import { useNotificationStore } from "@/modules/notifications/stores/notifications";

import useLoading from "@/composables/useLoading";
import { getServiceByBasename } from "@/services";
import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "NotificationListView",
  metaInfo: {
    title: "Notificaciones",
  },
  filters: {
    datetime: isoDateTimeToLocaleString,
  },
  setup(props, { refs }) {
    // Store
    const notificationStore = useNotificationStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });

    // State
    const modelClass = Notification;
    const service = getServiceByBasename(Notification.serviceBasename);
    const tableHeaders = [
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
    ];
    const tableOptions = {
      sortBy: ["unread", "timestamp"],
      sortDesc: [true, true],
      multiSort: true,
    };
    const filterComponent = NotificationFilters;
    const levelIcons = {
      success: "mdi-check",
      info: "mdi-information",
      warning: "mdi-exclamation",
      error: "mdi-alert",
    };

    // Computed
    const { notificationTargetMap } = toRefs(notificationStore);

    // Methods
    async function performBulkAction(actionFunctionName, selectedItems) {
      addTask("bulk-action", actionFunctionName);
      try {
        const params = { id__in: selectedItems.map((item) => item.id).join(",") };
        await service[actionFunctionName](params);
        refs.itemIndex.fetchTableItems();
        notificationStore.getUnreadCount();
      } finally {
        removeTask("bulk-action", actionFunctionName);
      }
    }
    function openDeleteDialog(selectedItems) {
      refs.deleteDialog.open(selectedItems);
    }

    return {
      // State
      modelClass,
      tableHeaders,
      tableOptions,
      filterComponent,
      levelIcons,
      // Computed
      isLoading,
      notificationTargetMap,
      // Methods
      isTaskLoading,
      performBulkAction,
      openDeleteDialog,
    };
  },
};
</script>
