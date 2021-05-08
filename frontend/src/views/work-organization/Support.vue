<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-namespace="support"
          verbose-name="Jornada de soporte"
          verbose-name-plural="Jornadas de soporte"
          item-text="date"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :quick-filters="quickFilters"
          default-quick-filter="next-days"
          :service="service"
          :form-component="formComponent"
        >
          <template #item.date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.user="{ value }">
            <UserPill :user="value" />
          </template>

          <template #fab="{ canCreate }">
            <v-btn
              v-if="canCreate(loggedUser)"
              fab
              fixed
              bottom
              right
              color="secondary"
              @click.stop="$refs.supportDayBulkForm.open()"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <StepperBulkFormDialog
      v-if="loggedUser.is_superuser"
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

import SupportService from "@/services/work-organization/support-service";

import StepperBulkFormDialog from "@/components/work-organization/dialogs/StepperBulkFormDialog";
import SupportDayBulkForm from "@/components/work-organization/support/forms/SupportDayBulkForm";
import SupportDayForm from "@/components/work-organization/support/forms/SupportDayForm";
import SupportFilters from "@/components/work-organization/support/SupportFilters";

export default {
  name: "Support",
  metaInfo: {
    title: "Soporte",
  },
  components: { StepperBulkFormDialog },
  data() {
    return {
      tableOptions: {
        sortBy: ["date"],
        sortDesc: [false],
        mustSort: true,
      },
      service: SupportService,
      filterComponent: SupportFilters,
      formComponent: SupportDayForm,
      bulkFormComponent: SupportDayBulkForm,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
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
      return this.loggedUser.is_superuser ? adminOptions : defaultOptions;
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
