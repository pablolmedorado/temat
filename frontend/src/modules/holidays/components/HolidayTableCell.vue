<template>
  <td :style="cellStyle">
    <v-menu v-if="holiday" :disabled="!canManage" right offset-x>
      <template #activator="{ on }">
        <v-btn icon small :loading="isLoading" v-on="on">
          <v-icon small>{{ cellIcon }}</v-icon>
        </v-btn>
      </template>
      <v-list dense>
        <v-list-item v-for="item in menuItems" :key="item.label" @click="item.action">
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ item.label }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-menu>
  </td>
</template>

<script>
import { computed } from "@vue/composition-api";
import colors from "vuetify/lib/util/colors";

import Holiday from "@/modules/holidays/models/holiday";

import useHolidays from "@/modules/holidays/composables/useHolidays";
import useLoading from "@/composables/useLoading";
import { hex2rgba } from "@/utils/colours";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "HolidayTableCell",
  props: {
    date: {
      type: String,
      required: true,
    },
    holiday: {
      type: Object,
      default: undefined,
    },
  },
  setup(props, { emit }) {
    // Composables
    const { isLoading, addTask, removeTask } = useLoading();
    const { edit, cancel, getStatusInfo } = useHolidays();

    // State
    const canManage = userHasPermission(Holiday.CHANGE_PERMISSION);

    // Computed
    const cellStyle = computed(() => {
      if (props.holiday) {
        const colorName = getStatusInfo(props.holiday.approved).colour;
        return { background: hex2rgba(colors[colorName].base, 0.5) };
      }
      return {};
    });
    const cellIcon = computed(() => {
      if (props.holiday) {
        return getStatusInfo(props.holiday.approved).icon;
      }
      return undefined;
    });
    const menuItems = computed(() => {
      if (props.holiday) {
        const items = [
          { key: "cancel", icon: "mdi-delete", label: "Cancelar", action: () => cancelHoliday(props.holiday) },
        ];
        if (props.holiday.approved !== false) {
          items.unshift({
            key: "deny",
            icon: "mdi-cancel",
            label: "Denegar",
            action: () => editHoliday(props.holiday, false),
          });
        }
        if (props.holiday.approved !== true) {
          items.unshift({
            key: "approve",
            icon: "mdi-check",
            label: "Aprobar",
            action: () => editHoliday(props.holiday, true),
          });
        }
        return items;
      }
      return [];
    });

    // Methods
    async function editHoliday(item, approved) {
      addTask(`edit-holiday-${approved}`, item.id);
      try {
        const response = await edit(item, approved);
        emit("change:holiday", response.data);
      } finally {
        removeTask(`edit-holiday-${approved}`, item.id);
      }
    }
    async function cancelHoliday(item) {
      addTask("cancel-holiday", item.id);
      try {
        const response = await cancel(item);
        if (response) {
          emit("change:holiday", response.data);
        }
      } finally {
        removeTask("cancel-holiday", item.id);
      }
    }

    return {
      // State
      canManage,
      // Computed
      isLoading,
      cellStyle,
      cellIcon,
      menuItems,
    };
  },
};
</script>

<style lang="scss" scoped>
td {
  min-width: 60px;
}
</style>
