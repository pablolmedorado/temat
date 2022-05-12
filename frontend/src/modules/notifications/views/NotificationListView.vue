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
            <v-menu bottom left offset-y>
              <template #activator="{ attrs, on }">
                <v-btn v-bind="attrs" :disabled="isLoading" icon v-on="on">
                  <v-badge
                    :value="Boolean(selectedItems.length)"
                    color="secondary"
                    :content="selectedItems.length.toString()"
                    overlap
                  >
                    <v-icon>mdi-dots-vertical</v-icon>
                  </v-badge>
                </v-btn>
              </template>
              <v-list dense>
                <template v-if="!Boolean(selectedItems.length)">
                  <v-list-item @click="performBulkAction('markAllAsRead', [])">
                    <v-list-item-icon>
                      <v-icon>mdi-email-open</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Marcar todo como leído</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click.stop="openDeleteDialog([])">
                    <v-list-item-icon>
                      <v-icon>mdi-delete</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Eliminar todo</v-list-item-title>
                  </v-list-item>
                </template>
                <template v-else>
                  <v-list-item @click="performBulkAction('markAllAsRead', selectedItems)">
                    <v-list-item-icon>
                      <v-icon>mdi-email-open</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Marcar como leído</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click="performBulkAction('markAllAsUnread', selectedItems)">
                    <v-list-item-icon>
                      <v-icon>mdi-email-mark-as-unread</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Marcar como no leído</v-list-item-title>
                  </v-list-item>
                  <v-list-item @click.stop="openDeleteDialog(selectedItems)">
                    <v-list-item-icon>
                      <v-icon>mdi-delete</v-icon>
                    </v-list-item-icon>
                    <v-list-item-title>Eliminar</v-list-item-title>
                  </v-list-item>
                </template>
              </v-list>
            </v-menu>
            <v-divider vertical inset class="mx-1" />
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

import { useLoading } from "@/composables/loading";
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
