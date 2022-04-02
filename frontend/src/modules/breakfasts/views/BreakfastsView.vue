<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          :model-class="modelClass"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :table-footer-props="tableFooterProps"
          custom-headers
          selectable-rows
        >
          <template #toolbar="{ isIndexLoading }">
            <v-tooltip bottom>
              <template #activator="{ attrs, on }">
                <v-btn
                  icon
                  v-bind="attrs"
                  :disabled="isIndexLoading"
                  :loading="isTaskLoading('fetch-user-breakfast')"
                  v-on="on"
                  @click.stop="openFormDialog"
                >
                  <v-icon>mdi-account</v-icon>
                </v-btn>
              </template>
              <span>Mi desayuno</span>
            </v-tooltip>
          </template>

          <template #item.user="{ value }">
            <UserPill :user="value" />
          </template>

          <template #fab="{ selectedItems }">
            <v-fab-transition>
              <v-btn
                v-show="selectedItems.length"
                fab
                fixed
                bottom
                right
                color="secondary"
                @click.stop="$refs.breakfastSummaryDialog.open(selectedItems)"
              >
                <v-icon>mdi-clipboard-list</v-icon>
              </v-btn>
            </v-fab-transition>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <FormDialog ref="formDialog" verbose-name="Desayuno" :form-component="formComponent" @submit="onFormSubmit" />

    <BreakfastSummaryDialog ref="breakfastSummaryDialog" />
  </v-container>
</template>

<script>
import Breakfast from "@/modules/breakfasts/models/breakfast";

import BreakfastForm from "@/modules/breakfasts/components/forms/BreakfastForm";
import BreakfastSummaryDialog from "@/modules/breakfasts/components/dialogs/BreakfastSummaryDialog";

import { useMainStore } from "@/stores/main";

import useLoading from "@/composables/useLoading";
import { getServiceByBasename } from "@/services";

export default {
  name: "BreakfastsView",
  metaInfo: {
    title: "Desayunos",
  },
  components: { BreakfastSummaryDialog },
  setup(props, { refs }) {
    // Store
    const store = useMainStore();

    // Composables
    const { addTask, removeTask, isTaskLoading } = useLoading();

    // State
    const modelClass = Breakfast;
    const service = getServiceByBasename(modelClass.serviceBasename);
    const tableHeaders = [
      {
        text: "Usuario",
        align: "start",
        sortable: true,
        value: "user",
        sortingField: "user__acronym",
        fixed: true,
      },
      { text: "Pan", align: "start", sortable: true, value: "bread.name", sortingField: "bread__name", fixed: true },
      { text: "Base", align: "start", sortable: true, value: "base.name", sortingField: "base__name", fixed: true },
      {
        text: "Primer ingrediente",
        align: "start",
        sortable: true,
        value: "ingredient1.name",
        sortingField: "ingredient1__name",
        fixed: true,
      },
      {
        text: "Segundo ingrediente",
        align: "start",
        sortable: true,
        value: "ingredient2.name",
        sortingField: "ingredient2__name",
        fixed: true,
      },
      { text: "Bebida", align: "start", sortable: true, value: "drink.name", sortingField: "drink__name" },
    ];
    const tableOptions = {
      itemsPerPage: -1,
      sortBy: ["user"],
      sortDesc: [false],
      multiSort: true,
    };
    const tableFooterProps = {
      itemsPerPageOptions: [10, 25, 50, -1],
    };
    const formComponent = BreakfastForm;

    // Methods
    async function getUserBreakfast() {
      addTask("fetch-user-breakfast");
      try {
        const response = await service.list({
          user_id: store.currentUser.id,
          page_size: 1,
          page: 1,
        });
        return response.data.results.length ? response.data.results[0] : modelClass.getDefaults();
      } finally {
        removeTask("fetch-user-breakfast");
      }
    }
    async function openFormDialog() {
      const userBreakfast = await getUserBreakfast();
      refs.formDialog.open(userBreakfast);
    }
    function onFormSubmit() {
      refs.itemIndex.fetchTableItems();
    }

    return {
      // Composables
      isTaskLoading,
      // State
      modelClass,
      tableHeaders,
      tableOptions,
      tableFooterProps,
      formComponent,
      // Methods
      openFormDialog,
      onFormSubmit,
    };
  },
};
</script>
