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
import { mapState } from "vuex";
import { DateTime } from "luxon";

import SupportWorkingDay from "@/modules/support-working-days/models/support-working-day";

import StepperBulkFormDialog from "@/components/dialogs/StepperBulkFormDialog";
import SupportDayBulkForm from "@/modules/support-working-days/components/forms/SupportDayBulkForm";
import SupportDayForm from "@/modules/support-working-days/components/forms/SupportDayForm";
import SupportFilters from "@/modules/support-working-days/components/filters/SupportFilters";

import { userHasPermission, userHasAnyPermission } from "@/utils/permissions";

export default {
  name: "SupportListView",
  metaInfo: {
    title: "Soporte",
  },
  components: { StepperBulkFormDialog },
  data() {
    return {
      modelClass: SupportWorkingDay,
      tableOptions: {
        sortBy: ["date"],
        sortDesc: [false],
        mustSort: true,
      },
      filterComponent: SupportFilters,
      formComponent: SupportDayForm,
      bulkFormComponent: SupportDayBulkForm,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    canAdd() {
      return userHasPermission(this.modelClass.ADD_PERMISSION);
    },
    tableHeaders() {
      const defaultOptions = [
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
      const adminOptions = [
        ...defaultOptions,
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true },
      ];
      return userHasAnyPermission([this.modelClass.CHANGE_PERMISSION, this.modelClass.DELETE_PERMISSION])
        ? adminOptions
        : defaultOptions;
    },
    quickFilters() {
      return [
        { key: "next-days", label: "Próximas jornadas", filters: { date__gte: DateTime.local().toISODate() } },
        {
          key: "my-next-days",
          label: "Mis próximas jornadas",
          filters: { date__gte: DateTime.local().toISODate(), user_id: this.loggedUser.id },
        },
      ];
    },
  },
  methods: {
    fetchTableItems() {
      this.$refs.itemIndex.fetchTableItems();
    },
  },
};
</script>
