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
      <template #activator="{ on: menu }">
        <v-tooltip bottom>
          <template #activator="{ on: tooltip }">
            <v-btn icon v-on="{ ...tooltip, ...menu }">
              <v-badge :color="unreadCountBadgeColour" :content="unreadCount | text" bordered overlap>
                <v-icon>{{ areNotificationsEnabled ? "mdi-bell-ring" : "mdi-bell" }}</v-icon>
              </v-badge>
            </v-btn>
          </template>
          <span> Notificaciones </span>
        </v-tooltip>
      </template>

      <v-card :loading="loadingNotificationSummary">
        <v-toolbar flat dense>
          <v-toolbar-title>
            Notificaciones{{ unreadCount > notifications.length ? ` (${notifications.length}/${unreadCount})` : "" }}
          </v-toolbar-title>
          <v-spacer />
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-btn
                icon
                :disabled="!Boolean(notificationPartition[0].length)"
                v-bind="attrs"
                @click="markAllNotificationsAsRead"
                v-on="on"
              >
                <v-icon>mdi-notification-clear-all</v-icon>
              </v-btn>
            </template>
            <span> Marcar todas como leídas </span>
          </v-tooltip>
          <v-btn icon @click="getUnreadSummary">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-toolbar>
        <v-card-text class="pa-0">
          <template v-if="!loadingNotificationSummary">
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
                            :disabled="!notification.unread"
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
          <v-btn color="primary" text :to="{ name: 'notifications' }" @click="showNotificationSummary = false">
            Ver todas
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-menu>
  </div>
</template>

<script>
import { mapGetters, mapMutations, mapState } from "vuex";
import { createNamespacedHelpers } from "vuex-composition-helpers";
import { useIntervalFn } from "@vueuse/core";
import { isNil, partition } from "lodash";

import NotificationService from "@/services/common/notification-service";

import useNotifications from "@/composables/useNotifications";

import NotificationImg from "@/assets/notification.png";

export default {
  name: "NotificationManager",
  filters: {
    text: function (value) {
      return isNil(value) ? "" : value.toString();
    },
  },
  setup() {
    const { useActions } = createNamespacedHelpers("notifications");
    const { getUnreadCount } = useActions(["getUnreadCount"]);

    const { areEnabled: areNotificationsEnabled } = useNotifications();
    useIntervalFn(() => getUnreadCount(), 300000, true); // 5 minutes

    return {
      areNotificationsEnabled,
      getUnreadCount,
    };
  },
  data() {
    return {
      updateInterval: null,
      showNotificationSummary: false,
      loadingNotificationSummary: false,
      notifications: [],
    };
  },
  computed: {
    ...mapState("notifications", ["unreadCount"]),
    ...mapGetters("notifications", ["notificationTargetMap", "unreadCountBadgeColour"]),
    notificationPartition() {
      return partition(this.notifications, { unread: true });
    },
  },
  watch: {
    unreadCount(newValue, oldValue) {
      if (this.areNotificationsEnabled && newValue > oldValue) {
        new Notification("TeMaT", {
          body: `Tienes ${newValue} notificación/es sin leer`,
          icon: NotificationImg,
        });
      }
    },
    showNotificationSummary(newValue) {
      if (newValue) {
        this.getUnreadSummary();
      } else {
        this.notifications = [];
      }
    },
  },
  created() {
    this.getUnreadCount();
  },
  methods: {
    ...mapMutations("notifications", ["setUnreadCount"]),
    async getUnreadSummary() {
      this.loadingNotificationSummary = true;
      try {
        const response = await NotificationService.unreadSummary();
        this.notifications = response.data.results;
        this.setUnreadCount(response.data.count);
      } finally {
        this.loadingNotificationSummary = false;
      }
    },
    async markNotificationAsRead(id) {
      const response = await NotificationService.markAsRead(id);
      const notification = response.data;
      const notificationIndex = this.notifications.findIndex((item) => item.id === notification.id);
      this.notifications.splice(notificationIndex, 1, notification);
      this.getUnreadCount();
    },
    async markAllNotificationsAsRead() {
      if (this.notificationPartition[0].length) {
        const notificationIds = this.notificationPartition[0].map((notification) => notification.id);
        await NotificationService.markSummaryAsRead({ id__in: notificationIds.join(",") });
        this.getUnreadSummary();
      }
    },
    getNotificationIcon(notification) {
      return notification.target ? this.notificationTargetMap[notification.target_content_type].icon : "mdi-bell-alert";
    },
    navigateToTarget(notification) {
      if (notification.unread) {
        this.markNotificationAsRead(notification.id);
      }
      this.$router.push({
        ...this.notificationTargetMap[notification.target_content_type].route,
        params: { id: notification.target.id },
      });
      this.showNotificationSummary = false;
    },
  },
};
</script>

<style lang="scss" scoped>
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
