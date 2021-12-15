<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :quick-filters="quickFilters"
          default-quick-filter="current-year"
          :form-component="formComponent"
          :allow-add="modelClass.ADD_PERMISSION"
          :allow-change="modelClass.CHANGE_PERMISSION"
          :allow-delete="modelClass.DELETE_PERMISSION"
          :disable-row-edition="isLoading"
          custom-headers
          reactive-filters
        >
          <template #title="{ verboseNamePlural, filters }">
            <span>{{ verboseNamePlural }}&nbsp;({{ filters.date__year }})</span>
          </template>

          <template #toolbar="{ isIndexLoading }">
            <v-menu bottom left offset-y>
              <template #activator="{ on: menu }">
                <v-tooltip bottom>
                  <template #activator="{ on: tooltip }">
                    <v-btn icon :disabled="isIndexLoading" v-on="{ ...tooltip, ...menu }">
                      <v-icon>mdi-calendar-range</v-icon>
                    </v-btn>
                  </template>
                  <span>Año</span>
                </v-tooltip>
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
              <v-btn icon :disabled="isLoading" @click.stop="$refs.volunteersDialog.open(item)">
                <v-icon>mdi-account-multiple</v-icon>
              </v-btn>
            </v-badge>
            <v-btn
              icon
              :disabled="isLoading"
              :loading="isTaskLoading('toggle-volunteer', item.id)"
              @click="toggleVolunteer(item)"
            >
              <v-icon>
                {{ item.volunteers.includes(loggedUser.id) ? "mdi-account-remove" : "mdi-account-plus-outline" }}
              </v-icon>
            </v-btn>
          </template>

          <template #fab>
            <v-btn
              v-if="canAdd"
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
      v-if="canAdd"
      ref="greenWorkingDayBulkForm"
      :max-width="1000"
      :form-component="bulkFormComponent"
      @submit="fetchTableItems"
    >
      <template #header>Crear jornadas especiales</template>
    </StepperBulkFormDialog>
  </v-container>
</template>

<script>
import { mapActions, mapState } from "pinia";
import { DateTime } from "luxon";

import GreenWorkingDay from "@/modules/green-working-days/models/green-working-day";

import StepperBulkFormDialog from "@/components/dialogs/StepperBulkFormDialog";
import GreenWorkingDayBulkForm from "@/modules/green-working-days/components/forms/GreenWorkingDayBulkForm";
import GreenWorkingDayForm from "@/modules/green-working-days/components/forms/GreenWorkingDayForm";
import VoluteersDialog from "@/modules/green-working-days/components/dialogs/VoluteersDialog";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import { getServiceByBasename } from "@/services";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "GreenWorkingDayListView",
  metaInfo: {
    title: "Jornadas especiales",
  },
  components: { StepperBulkFormDialog, VoluteersDialog },
  setup() {
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });
    return { isLoading, isTaskLoading, addTask, removeTask };
  },
  data() {
    return {
      modelClass: GreenWorkingDay,
      service: getServiceByBasename(GreenWorkingDay.serviceBasename),
      tableHeaders: [
        { text: "Fecha", align: "start", sortable: true, value: "date", fixed: true },
        { text: "Etiqueta", align: "start", sortable: true, value: "label", default: true },
        {
          text: "Usuario principal",
          align: "start",
          sortable: true,
          value: "main_user",
          sortingField: "main_user__acronym",
          fixed: true,
        },
        {
          text: "Usuario de apoyo",
          align: "start",
          sortable: true,
          value: "support_user",
          sortingField: "support_user__acronym",
          default: true,
        },
        {
          text: "Acciones",
          align: "start",
          sortable: false,
          value: "table_actions",
          fields: ["volunteers"],
          fixed: true,
        },
      ],
      tableOptions: {
        sortBy: ["date"],
        sortDesc: [false],
        mustSort: true,
      },
      quickFilters: [{ key: "current-year", label: "Año en curso", filters: { date__year: DateTime.local().year } }],
      formComponent: GreenWorkingDayForm,
      bulkFormComponent: GreenWorkingDayBulkForm,
    };
  },
  computed: {
    ...mapState(useMainStore, ["loggedUser", "yearOptions"]),
    canAdd() {
      return userHasPermission(this.modelClass.ADD_PERMISSION);
    },
  },
  methods: {
    ...mapActions(useMainStore, ["showSnackbar"]),
    fetchTableItems() {
      this.$refs.itemIndex.fetchTableItems();
    },
    async toggleVolunteer(item) {
      this.addTask("toggle-volunteer", item.id);
      try {
        await this.service.toggleVolunteer(item.id);
        this.fetchTableItems();
        this.showSnackbar({
          color: "success",
          message: "Estado de voluntario actualizado correctamente",
        });
      } finally {
        this.removeTask("toggle-volunteer", item.id);
      }
    },
    setYearFilter(year) {
      this.$refs.itemIndex.addFilter({ date__year: year });
      this.$nextTick(() => {
        this.$refs.itemIndex.fetchTableItems();
      });
    },
  },
};
</script>
