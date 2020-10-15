<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <ItemIndex
          ref="itemIndex"
          local-storage-key="breakfast"
          verbose-name="Desayuno"
          verbose-name-plural="Desayunos"
          :table-available-headers="tableHeaders"
          :table-initial-options="tableOptions"
          :table-footer-props="tableFooterProps"
          :service="service"
          :form-component="formComponent"
          :default-item="defaultItem"
          :clear-form-item-on-finish="false"
          :can-create="() => false"
          custom-headers
          selectable-rows
        >
          <template #toolbar>
            <v-tooltip bottom>
              <template #activator="{ attrs, on }">
                <v-btn
                  icon
                  v-bind="attrs"
                  :disabled="loading"
                  :loading="loadingUserBreakfast"
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
                @click.stop="$refs.breakfastsSummaryDialog.open(selectedItems)"
              >
                <v-icon>mdi-clipboard-list</v-icon>
              </v-btn>
            </v-fab-transition>
          </template>
        </ItemIndex>
      </v-col>
    </v-row>

    <BreakfastsSummaryDialog ref="breakfastsSummaryDialog" />
  </v-container>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import BreakfastService from "@/services/breakfasts/breakfast-service";

import BreakfastForm from "@/components/breakfasts/BreakfastForm";
import BreakfastsSummaryDialog from "@/components/breakfasts/BreakfastsSummaryDialog";

export default {
  name: "Breakfasts",
  components: { BreakfastsSummaryDialog },
  data() {
    return {
      tableHeaders: [
        {
          text: "Usuario",
          align: "start",
          sortable: true,
          value: "user",
          sortingField: "user__acronym",
          fixed: true
        },
        { text: "Pan", align: "start", sortable: true, value: "bread.name", sortingField: "bread__name", fixed: true },
        { text: "Base", align: "start", sortable: true, value: "base.name", sortingField: "base__name", fixed: true },
        {
          text: "Primer ingrediente",
          align: "start",
          sortable: true,
          value: "ingredient1.name",
          sortingField: "ingredient1__name",
          fixed: true
        },
        {
          text: "Segundo ingrediente",
          align: "start",
          sortable: true,
          value: "ingredient2.name",
          sortingField: "ingredient2__name",
          fixed: true
        },
        { text: "Bebida", align: "start", sortable: true, value: "drink.name", sortingField: "drink__name" }
      ],
      tableOptions: {
        itemsPerPage: -1,
        sortBy: ["user"],
        sortDesc: [false],
        multiSort: true
      },
      tableFooterProps: {
        itemsPerPageOptions: [10, 25, 50, -1]
      },
      service: BreakfastService,
      formComponent: BreakfastForm,
      loadingUserBreakfast: false
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["loading"]),
    defaultItem() {
      return {
        id: null,
        user: this.loggedUser.id,
        bread: null,
        base: null,
        ingredient1: null,
        ingredient2: null,
        drink: null
      };
    }
  },
  methods: {
    async getUserBreakfast() {
      this.loadingUserBreakfast = true;
      try {
        const response = await this.service.list({
          user_id: this.loggedUser.id,
          page_size: 1,
          page: 1
        });
        return response.data.results.length ? response.data.results[0] : null;
      } finally {
        this.loadingUserBreakfast = false;
      }
    },
    async openFormDialog() {
      const userBreakfast = await this.getUserBreakfast();
      this.$refs.itemIndex.openFormDialog(userBreakfast);
    }
  }
};
</script>
