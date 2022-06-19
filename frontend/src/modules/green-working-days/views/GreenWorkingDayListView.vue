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
          <template #item.users="{ value }">
            <template v-if="!value.length"> No asignada </template>
            <UserPill v-for="user in value" v-else :key="user" :user="user" class="my-1 mr-2" />
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
                {{ item.volunteers.includes(currentUser.id) ? "mdi-account-remove" : "mdi-account-plus-outline" }}
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
import { nextTick, toRefs } from "@vue/composition-api";
import { DateTime } from "luxon";

import GreenWorkingDay from "@/modules/green-working-days/models/green-working-day";

import { useMainStore } from "@/stores/main";

import StepperBulkFormDialog from "@/components/dialogs/StepperBulkFormDialog";
import VoluteersDialog from "@/modules/green-working-days/components/dialogs/VoluteersDialog";
import GreenWorkingDayBulkForm from "@/modules/green-working-days/components/forms/GreenWorkingDayBulkForm";
import GreenWorkingDayForm from "@/modules/green-working-days/components/forms/GreenWorkingDayForm";

import { useLoading } from "@/composables/loading";

import { userHasPermission } from "@/utils/permissions";

import { getServiceByBasename } from "@/services";

export default {
  name: "GreenWorkingDayListView",
  metaInfo: {
    title: "Jornadas especiales",
  },
  components: { StepperBulkFormDialog, VoluteersDialog },
  setup(props, { refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading({
      includedChildren: ["itemIndex"],
    });

    // State
    const modelClass = GreenWorkingDay;
    const service = getServiceByBasename(GreenWorkingDay.serviceBasename);
    const tableHeaders = [
      { text: "Fecha", align: "start", sortable: true, value: "date", fixed: true },
      { text: "Etiqueta", align: "start", sortable: true, value: "label", default: true },
      {
        text: "Usuarios",
        align: "start",
        sortable: false,
        value: "users",
        fixed: true,
      },
      {
        text: "Acciones",
        align: "start",
        sortable: false,
        value: "table_actions",
        fields: ["volunteers"],
        fixed: true,
      },
    ];
    const tableOptions = {
      sortBy: ["date"],
      sortDesc: [false],
      mustSort: true,
    };
    const quickFilters = [
      { key: "current-year", label: "Año en curso", filters: { date__year: DateTime.local().year } },
    ];
    const formComponent = GreenWorkingDayForm;
    const bulkFormComponent = GreenWorkingDayBulkForm;
    const canAdd = userHasPermission(modelClass.ADD_PERMISSION);

    // Computed
    const { currentUser, yearOptions } = toRefs(store);

    // Methods
    function fetchTableItems() {
      refs.itemIndex.fetchTableItems();
    }
    async function toggleVolunteer(item) {
      addTask("toggle-volunteer", item.id);
      try {
        await service.toggleVolunteer(item.id);
        fetchTableItems();
        store.showSnackbar({
          color: "success",
          message: "Estado de voluntario actualizado correctamente",
        });
      } finally {
        removeTask("toggle-volunteer", item.id);
      }
    }
    function setYearFilter(year) {
      refs.itemIndex.addFilter({ date__year: year });
      nextTick(() => {
        fetchTableItems();
      });
    }

    return {
      // State
      modelClass,
      service,
      tableHeaders,
      tableOptions,
      quickFilters,
      formComponent,
      bulkFormComponent,
      canAdd,
      // Computed
      isLoading,
      currentUser,
      yearOptions,
      // Methods
      isTaskLoading,
      fetchTableItems,
      toggleVolunteer,
      setYearFilter,
    };
  },
};
</script>
