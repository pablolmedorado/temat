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
import { mapState } from "pinia";

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
  setup() {
    const { isLoading, addTask, removeTask, isTaskLoading } = useLoading();
    return {
      isLoading,
      addTask,
      removeTask,
      isTaskLoading,
    };
  },
  data() {
    return {
      modelClass: Breakfast,
      service: getServiceByBasename(Breakfast.serviceBasename),
      tableHeaders: [
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
      ],
      tableOptions: {
        itemsPerPage: -1,
        sortBy: ["user"],
        sortDesc: [false],
        multiSort: true,
      },
      tableFooterProps: {
        itemsPerPageOptions: [10, 25, 50, -1],
      },
      formComponent: BreakfastForm,
      loadingUserBreakfast: false,
    };
  },
  computed: {
    ...mapState(useMainStore, ["currentUser"]),
  },
  methods: {
    async getUserBreakfast() {
      this.addTask("fetch-user-breakfast");
      try {
        const response = await this.service.list({
          user_id: this.currentUser.id,
          page_size: 1,
          page: 1,
        });
        return response.data.results.length ? response.data.results[0] : this.modelClass.defaults;
      } finally {
        this.removeTask("fetch-user-breakfast");
      }
    },
    async openFormDialog() {
      const userBreakfast = await this.getUserBreakfast();
      this.$refs.formDialog.open(userBreakfast);
    },
    onFormSubmit() {
      this.$refs.itemIndex.fetchTableItems();
    },
  },
};
</script>
