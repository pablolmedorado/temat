<template>
  <v-dialog
    v-model="showDialog"
    v-bind="$attrs"
    :width="width"
    :max-width="1000"
    scrollable
    @click:outside="close"
    @keydown.esc="close"
  >
    <v-card>
      <v-card-text class="pa-0">
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :system-filters="systemFilters"
          :quick-filters="quickFilters"
          default-quick-filter="pending"
          :allow-add="false"
          :allow-change="false"
          :allow-delete="false"
          flat
        >
          <template #title> Gestión de vacaciones </template>

          <template #item.planned_date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.user="{ value }">
            <UserPill :user="value" />
          </template>
          <template #item.approved="{ value }">
            <v-chip :color="getHolidayStatusInfo(value).colour" dark>
              <v-icon small>{{ getHolidayStatusInfo(value).icon }}</v-icon>
            </v-chip>
          </template>
          <template #item.table_actions="{ item }">
            <span class="d-inline-flex">
              <v-btn
                v-show="[null, false].includes(item.approved)"
                :disabled="isLoading"
                :loading="isTaskLoading('edit-holiday-true', item.id)"
                icon
                @click="editHoliday(item, true)"
              >
                <v-icon>mdi-check</v-icon>
              </v-btn>
              <v-btn
                v-show="[null, true].includes(item.approved)"
                :disabled="isLoading"
                :loading="isTaskLoading('edit-holiday-false', item.id)"
                icon
                @click="editHoliday(item, false)"
              >
                <v-icon>mdi-cancel</v-icon>
              </v-btn>
              <v-btn
                :disabled="isLoading"
                :loading="isTaskLoading('cancel-holiday', item.id)"
                icon
                @click="cancelHoliday(item)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </span>
          </template>
        </ItemIndex>
      </v-card-text>
      <v-divider />
      <v-card-actions>
        <v-spacer />
        <v-btn text @click.stop="close">Volver</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { nextTick } from "@vue/composition-api";

import Holiday from "@/modules/holidays/models/holiday";

import HolidayFilters from "@/modules/holidays/components/filters/HolidayFilters";

import { useLoading } from "@/composables/loading";
import { useDialog, dialogProps } from "@/composables/dialog";
import { useHolidays } from "@/modules/holidays/composables/holidays";
import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "HolidayManagementDialog",
  props: dialogProps,
  setup(props, { emit, refs }) {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });

    // Table
    const tableOptions = {
      ...defaultTableOptions,
      sortBy: ["planned_date"],
      sortDesc: [false],
      multiSort: true,
    };
    const tableHeaders = [
      { text: "Fecha", align: "start", sortable: true, value: "planned_date", fixed: true },
      {
        text: "Usuario",
        align: "start",
        sortable: true,
        value: "user",
        sortingField: "user__acronym",
        fixed: true,
      },
      {
        text: "Estado",
        align: "start",
        sortable: true,
        value: "approved",
        fixed: true,
      },
      {
        text: "Acciones",
        align: "left",
        sortable: false,
        value: "table_actions",
        fixed: true,
      },
    ];
    const systemFilters = {
      planned_date__isnull: false,
    };
    const quickFilters = [
      {
        key: "pending",
        label: "Pendientes",
        filters: { approved__isnull: true },
      },
    ];
    function fetchItems() {
      refs.itemIndex.fetchTableItems();
    }

    // Holidays
    const { edit, cancel, getStatusInfo } = useHolidays();
    async function editHoliday(item, approved) {
      addTask(`edit-holiday-${approved}`, item.id);
      try {
        const response = await edit(item, approved);
        emit("change:holiday", response.data);
        fetchItems();
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
          fetchItems();
        }
      } finally {
        removeTask("cancel-holiday", item.id);
      }
    }

    // Dialog
    const { showDialog, open: _open, close } = useDialog();
    function open() {
      _open();
      nextTick(() => {
        fetchItems();
      });
    }

    return {
      isLoading,
      isTaskLoading,
      // Table
      modelClass: Holiday,
      tableOptions,
      tableHeaders,
      filterComponent: HolidayFilters,
      systemFilters,
      quickFilters,
      fetchItems,
      // Holidays
      editHoliday,
      cancelHoliday,
      getHolidayStatusInfo: getStatusInfo,
      // Dialog
      showDialog,
      open,
      close,
    };
  },
};
</script>
