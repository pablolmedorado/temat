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
          :quick-filters="quickFilters"
          default-quick-filter="next-days"
          :form-component="formComponent"
          :allow-add="modelClass.ADD_PERMISSION"
          :allow-change="modelClass.CHANGE_PERMISSION"
          :allow-delete="modelClass.DELETE_PERMISSION"
        >
          <template #item.date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.user="{ value }">
            <UserPill :user="value" />
          </template>

          <template #fab>
            <v-btn v-if="canAdd" fab fixed bottom right color="secondary" @click.stop="$refs.supportDayBulkForm.open()">
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <StepperBulkFormDialog
      v-if="canAdd"
      ref="supportDayBulkForm"
      :form-component="bulkFormComponent"
      @submit="fetchTableItems"
    >
      <template #header>Crear jornadas de soporte</template>
    </StepperBulkFormDialog>
  </v-container>
</template>

<script>
import { computed } from "@vue/composition-api";
import { DateTime } from "luxon";

import SupportWorkingDay from "@/modules/support-working-days/models/support-working-day";

import StepperBulkFormDialog from "@/components/dialogs/StepperBulkFormDialog";
import SupportDayBulkForm from "@/modules/support-working-days/components/forms/SupportDayBulkForm";
import SupportDayForm from "@/modules/support-working-days/components/forms/SupportDayForm";
import SupportFilters from "@/modules/support-working-days/components/filters/SupportFilters";

import { useMainStore } from "@/stores/main";

import { userHasPermission, userHasAnyPermission } from "@/utils/permissions";

export default {
  name: "SupportListView",
  metaInfo: {
    title: "Soporte",
  },
  components: { StepperBulkFormDialog },
  setup(props, { refs }) {
    // Store
    const store = useMainStore();

    // State
    const modelClass = SupportWorkingDay;
    const defaultTableHeaders = [
      { text: "Fecha", align: "start", sortable: true, value: "date", fixed: true },
      {
        text: "Usuario",
        align: "start",
        sortable: true,
        value: "user",
        sortingField: "user__acronym",
        fixed: true,
      },
    ];
    const adminTableHeaders = [
      ...defaultTableHeaders,
      { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
    ];
    const tableOptions = {
      sortBy: ["date"],
      sortDesc: [false],
      mustSort: true,
    };
    const filterComponent = SupportFilters;
    const quickFilters = [
      { key: "next-days", label: "Próximas jornadas", filters: { date__gte: DateTime.local().toISODate() } },
      {
        key: "my-next-days",
        label: "Mis próximas jornadas",
        filters: { date__gte: DateTime.local().toISODate(), user_id: store.currentUser.id },
      },
    ];
    const formComponent = SupportDayForm;
    const bulkFormComponent = SupportDayBulkForm;

    // Computed
    const canAdd = computed(() => userHasPermission(modelClass.ADD_PERMISSION));
    const tableHeaders = computed(() => {
      return userHasAnyPermission([modelClass.CHANGE_PERMISSION, modelClass.DELETE_PERMISSION])
        ? adminTableHeaders
        : defaultTableHeaders;
    });

    // Methods
    function fetchTableItems() {
      refs.itemIndex.fetchTableItems();
    }

    return {
      // State
      modelClass,
      tableOptions,
      filterComponent,
      quickFilters,
      formComponent,
      bulkFormComponent,
      // Computed
      canAdd,
      tableHeaders,
      // Methods
      fetchTableItems,
    };
  },
};
</script>
