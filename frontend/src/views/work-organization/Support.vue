<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-key="support"
          verbose-name="Jornada de soporte"
          verbose-name-plural="Jornadas de soporte"
          item-text="date"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :filter-component="filterComponent"
          :default-filters="defaultFilters"
          :service="service"
          :form-component="formComponent"
        >
          <template v-slot:item.date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template v-slot:item.user="{ value }">
            <UserPill :user="value" />
          </template>

          <template v-slot:fab="{ canCreate }">
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
      v-if="loggedUser.is_staff"
      ref="supportDayBulkForm"
      :form-component="bulkFormComponent"
      @submit="fetchTableItems"
    >
      <template v-slot:header>Crear jornadas de soporte</template>
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
  components: { StepperBulkFormDialog },
  data() {
    return {
      tableOptions: {
        sortBy: ["date"],
        sortDesc: [false],
        mustSort: true
      },
      service: SupportService,
      filterComponent: SupportFilters,
      defaultFilters: {
        date__gte: DateTime.local().toISODate()
      },
      formComponent: SupportDayForm,
      bulkFormComponent: SupportDayBulkForm
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
          fixed: true
        }
      ];
      const adminOptions = [
        ...defaultOptions,
        { text: "Acciones", align: "start", sortable: false, value: "table_actions", fixed: true }
      ];
      return this.loggedUser.is_staff ? adminOptions : defaultOptions;
    }
  },
  methods: {
    fetchTableItems() {
      this.$refs.itemIndex.fetchTableItems();
    }
  }
};
</script>
