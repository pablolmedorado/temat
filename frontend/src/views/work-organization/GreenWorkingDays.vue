<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-key="greenWorkingDay"
          verbose-name="Jornada especial"
          verbose-name-plural="Jornadas especiales"
          item-text="date"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :default-filters="defaultFilters"
          :service="service"
          :form-component="formComponent"
          custom-headers
          reactive-filters
        >
          <template #title="{ verboseNamePlural, filters }">
            <span>{{ verboseNamePlural }}&nbsp;({{ filters.date__year }})</span>
          </template>

          <template #toolbar>
            <v-menu bottom left offset-y>
              <template #activator="{ on, attrs }">
                <v-btn icon :disabled="loading" v-bind="attrs" v-on="on">
                  <v-icon>mdi-calendar-range</v-icon>
                </v-btn>
              </template>
              <v-list>
                <v-list-item v-for="item in yearOptions" :key="item" @click="setYearFilter(item)">
                  <v-list-item-title>{{ item }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </template>

          <template #item.date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.main_user="{ value }">
            <UserPill v-if="value" :user="value" />
          </template>
          <template #item.support_user="{ value }">
            <UserPill v-if="value" :user="value" />
          </template>
          <template #item.table_actions="{ item }">
            <v-badge bottom left overlap>
              <template #badge>{{ item.volunteers.length }}</template>
              <v-btn icon @click.stop="$refs.volunteersDialog.open(item)">
                <v-icon>mdi-account-multiple</v-icon>
              </v-btn>
            </v-badge>
            <v-btn icon :disabled="loading" @click="toggleVolunteer(item.id)">
              <v-icon>
                {{ item.volunteers.includes(loggedUser.id) ? "mdi-account-remove" : "mdi-account-plus-outline" }}
              </v-icon>
            </v-btn>
          </template>

          <template #fab="{ canCreate }">
            <v-btn
              v-if="canCreate(loggedUser)"
              fab
              fixed
              bottom
              right
              color="secondary"
              @click.stop="$refs.greenWorkingDayBulkForm.open()"
            >
              <v-icon>mdi-plus</v-icon>
            </v-btn>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <VoluteersDialog ref="volunteersDialog" />

    <StepperBulkFormDialog
      v-if="loggedUser.is_staff"
      ref="greenWorkingDayBulkForm"
      :max-width="900"
      :form-component="bulkFormComponent"
      @submit="fetchTableItems"
    >
      <template #header>Crear jornadas especiales</template>
    </StepperBulkFormDialog>
  </v-container>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";
import { DateTime } from "luxon";

import GreenService from "@/services/work-organization/green-service";

import StepperBulkFormDialog from "@/components/work-organization/dialogs/StepperBulkFormDialog";
import GreenWorkingDayBulkForm from "@/components/work-organization/green-working-days/forms/GreenWorkingDayBulkForm";
import GreenWorkingDayForm from "@/components/work-organization/green-working-days/forms/GreenWorkingDayForm";
import VoluteersDialog from "@/components/work-organization/green-working-days/VoluteersDialog";

export default {
  name: "GreenWorkingDays",
  components: { StepperBulkFormDialog, VoluteersDialog },
  data() {
    return {
      tableHeaders: [
        { text: "Fecha", align: "start", sortable: true, value: "date", fixed: true },
        { text: "Etiqueta", align: "start", sortable: true, value: "label", default: true },
        {
          text: "Usuario principal",
          align: "start",
          sortable: true,
          value: "main_user",
          sortingField: "main_user__acronym",
          fixed: true
        },
        {
          text: "Usuario de apoyo",
          align: "start",
          sortable: true,
          value: "support_user",
          sortingField: "support_user__acronym",
          default: true
        },
        {
          text: "Acciones",
          align: "start",
          sortable: false,
          value: "table_actions",
          fields: ["volunteers"],
          fixed: true
        }
      ],
      tableOptions: {
        sortBy: ["date"],
        sortDesc: [false],
        mustSort: true
      },
      service: GreenService,
      defaultFilters: {
        date__year: DateTime.local().year
      },
      formComponent: GreenWorkingDayForm,
      bulkFormComponent: GreenWorkingDayBulkForm
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["loading", "yearOptions"])
  },
  methods: {
    ...mapActions(["showSnackbar"]),
    fetchTableItems() {
      this.$refs.itemIndex.fetchTableItems();
    },
    async toggleVolunteer(id) {
      await this.service.toggleVolunteer(id);
      this.fetchTableItems();
      this.showSnackbar({
        color: "success",
        message: "Estado de voluntario actualizado correctamente"
      });
    },
    setYearFilter(year) {
      this.$refs.itemIndex.addFilter({ date__year: year });
      this.$nextTick(() => {
        this.$refs.itemIndex.fetchTableItems();
      });
    }
  }
};
</script>
