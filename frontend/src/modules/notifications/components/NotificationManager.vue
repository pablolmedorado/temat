<template>
  <div>
    <v-menu
      v-model="showNotificationSummary"
      content-class="v-dialog--scrollable"
      :min-width="400"
      :max-width="400"
      :close-on-content-click="false"
      :nudge-width="200"
      bottom
      left
      offset-y
    >
      <template #activator="{ attrs: menuAttrs, on: menuOn }">
        <v-tooltip bottom>
          <template #activator="{ attrs: tooltipAttrs, on: tooltipOn }">
            <v-btn icon v-bind="{ ...tooltipAttrs, ...menuAttrs }" v-on="{ ...tooltipOn, ...menuOn }">
              <v-badge :color="unreadCountBadgeColour" :content="unreadCount | text" bordered overlap>
                <v-icon>{{ areNotificationsEnabled ? "mdi-bell-ring" : "mdi-bell" }}</v-icon>
              </v-badge>
            </v-btn>
          </template>
          <span> Notificaciones </span>
        </v-tooltip>
      </template>

      <v-card :loading="isTaskLoading('fetch-unread-summary')">
        <v-toolbar flat dense>
          <v-toolbar-title>
            Notificaciones{{ unreadCount > notifications.length ? ` (${notifications.length}/${unreadCount})` : "" }}
          </v-toolbar-title>
          <v-spacer />
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-btn
                icon
                :disabled="!Boolean(notificationPartition[0].length) || isLoading"
                :loading="isTaskLoading('mark-all-as-read')"
                v-bind="attrs"
                @click="markAllNotificationsAsRead"
                v-on="on"
              >
                <v-icon>mdi-notification-clear-all</v-icon>
              </v-btn>
            </template>
            <span> Marcar todas como leídas </span>
          </v-tooltip>
          <v-btn icon :disabled="isLoading" @click="getUnreadSummary">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="pa-0">
          <template v-if="!isTaskLoading('fetch-unread-summary')">
            <template v-if="notifications.length">
              <v-list v-for="(partition, index) in notificationPartition" :key="index" two-line class="pa-0">
                <template v-if="partition.length">
                  <v-subheader>{{ index === 0 ? "NUEVAS" : "Leídas" }}</v-subheader>
                  <v-list-item v-for="notification in partition" :key="notification.id">
                    <v-list-item-avatar :color="notification.level">
                      <v-icon dark>{{ getNotificationIcon(notification) }}</v-icon>
                    </v-list-item-avatar>
                    <v-list-item-content
                      :class="{ 'targeted-notification': notification.target }"
                      v-on="notification.target ? { click: () => navigateToTarget(notification) } : {}"
                    >
                      <v-list-item-title :class="{ 'font-weight-medium': index === 0 }">
                        {{ notification.actor.first_name }} {{ notification.actor.last_name }} {{ notification.verb }}
                        {{ notification.target ? `"${notification.target.representation}"` : "" }}
                      </v-list-item-title>
                      <v-list-item-subtitle>Hace {{ notification.timesince }}</v-list-item-subtitle>
                    </v-list-item-content>
                    <v-list-item-action v-if="notification.unread">
                      <v-tooltip bottom>
                        <template #activator="{ on }">
                          <v-btn
                            icon
                            :loading="isTaskLoading('mark-as-read', notification.id)"
                            @click="markNotificationAsRead(notification.id)"
                            v-on="on"
                          >
                            <v-icon>mdi-read</v-icon>
                          </v-btn>
                        </template>
                        <span> Marcar como leída </span>
                      </v-tooltip>
                    </v-list-item-action>
                  </v-list-item>
                </template>
              </v-list>
            </template>
            <template v-else>
              <v-alert class="mx-3 my-2" type="info" border="left" text outlined>
                No tienes notificaciones nuevas
              </v-alert>
            </template>
          </template>
          <template v-else>
            <v-skeleton-loader v-for="n in 3" :key="n" type="list-item-avatar-three-line" />
          </template>
        </v-card-text>
        <v-divider />
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="showNotificationSummary = false">Salir</v-btn>
          <v-btn text :to="{ name: 'notifications' }" @click="showNotificationSummary = false"> Ver todas </v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
import { computed, ref, toRefs, watch } from "@vue/composition-api";
import { useIntervalFn, useWebNotification } from "@vueuse/core";
import { isNil, partition } from "lodash-es";

import NotificationService from "@/modules/notifications/services/notification-service";

import { useMainStore } from "@/stores/main";
import { useNotificationStore } from "@/modules/notifications/stores/notifications";

import { useLoading } from "@/composables/loading";

import NotificationImg from "@/modules/notifications/assets/notification.png";

export default {
  name: "NotificationManager",
  filters: {
    text: function (value) {
      return isNil(value) ? "" : value.toString();
    },
  },
  setup(props, { root }) {
    // Store
    const mainStore = useMainStore();
    const notificationStore = useNotificationStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();
    const {
      isSupported: areNotificationsEnabled,
      show: showNotification,
      onClick: onNotificationClick,
    } = useWebNotification({
      title: mainStore.appName,
      lang: "es",
      icon: NotificationImg,
    });

    // State
    const showNotificationSummary = ref(false);
    const notifications = ref([]);

    // Computed
    const { unreadCount, unreadCountBadgeColour } = toRefs(notificationStore);
    const notificationPartition = computed(() => partition(notifications.value, { unread: true }));

    // Watchers
    watch(
      () => notificationStore.unreadCount,
      (newValue, oldValue) => {
        if (areNotificationsEnabled && newValue > oldValue) {
          showNotification({ body: `Tienes ${newValue} notificación/es sin leer` });
        }
      }
    );
    watch(showNotificationSummary, (newValue) => {
      if (newValue) {
        getUnreadSummary();
      } else {
        notifications.value = [];
      }
    });

    // Methods
    const getUnreadCount = notificationStore.getUnreadCount;
    async function getUnreadSummary() {
      addTask("fetch-unread-summary");
      try {
        const response = await NotificationService.unreadSummary();
        notifications.value = response.data.results;
        notificationStore.unreadCount = response.data.count;
      } finally {
        removeTask("fetch-unread-summary");
      }
    }
    async function markNotificationAsRead(id) {
      addTask("mark-as-read", id);
      try {
        const response = await NotificationService.markAsRead(id);
        const notification = response.data;
        const notificationIndex = notifications.value.findIndex((item) => item.id === notification.id);
        notifications.value.splice(notificationIndex, 1, notification);
        getUnreadCount();
      } finally {
        removeTask("mark-as-read", id);
      }
    }
    async function markAllNotificationsAsRead() {
      if (notificationPartition.value[0].length) {
        addTask("mark-all-as-read");
        try {
          const notificationIds = notificationPartition.value[0].map((notification) => notification.id);
          await NotificationService.markSummaryAsRead({ id__in: notificationIds.join(",") });
          getUnreadSummary();
        } finally {
          removeTask("mark-all-as-read");
        }
      }
    }
    function getNotificationIcon(notification) {
      return notification.target
        ? notificationStore.notificationTargetMap[notification.target_content_type].icon
        : "mdi-bell-alert";
    }
    function navigateToTarget(notification) {
      if (notification.unread) {
        markNotificationAsRead(notification.id);
      }
      root.$router.push({
        ...notificationStore.notificationTargetMap[notification.target_content_type].route,
        params: { id: notification.target.id },
      });
      showNotificationSummary.value = false;
    }

    // Initialization
    useIntervalFn(getUnreadCount, 300000, { immediate: true, immediateCallback: true }); // 5 minutes
    onNotificationClick.on(() => (showNotificationSummary.value = true));

    return {
      // State
      areNotificationsEnabled,
      showNotificationSummary,
      notifications,
      // Computed
      isLoading,
      unreadCount,
      unreadCountBadgeColour,
      notificationPartition,
      // Methods
      isTaskLoading,
      getUnreadSummary,
      markNotificationAsRead,
      markAllNotificationsAsRead,
      getNotificationIcon,
      navigateToTarget,
    };
  },
};
</script>

<style scoped>
.v-dialog--scrollable {
  max-height: 80%;
}
.v-list-item__title {
  white-space: unset;
}
.targeted-notification {
  cursor: pointer;
}
</style>
