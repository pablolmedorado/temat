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
          :system-filters="systemFilters"
          :quick-filters="quickFilters"
          default-quick-filter="last-week"
          :form-component="formComponent"
          :allow-change="(user, item) => canPerformAction(item, 'change')"
          :allow-delete="(user, item) => canPerformAction(item, 'delete')"
          custom-headers
        >
          <template #toolbar="{ filters, isIndexLoading }">
            <v-tooltip bottom>
              <template #activator="{ attrs, on }">
                <v-btn
                  icon
                  v-bind="attrs"
                  :disabled="isIndexLoading || !filters || !filters.date__gte || !filters.date__lte"
                  v-on="on"
                  @click.stop="openReportDialog(filters)"
                >
                  <v-icon>mdi-file-chart-outline</v-icon>
                </v-btn>
              </template>
              <span>Informe</span>
            </v-tooltip>
          </template>

          <template #item.date="{ value }">
            <DateRouterLink :date="value" />
          </template>
          <template #item.user_story="{ item }">
            <TruncatedText :value="item.user_story.name" :text-length="70" />
            <router-link class="ml-1 user-story-link" :to="{ name: 'user-story', params: { id: item.user_story.id } }">
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <v-icon small v-bind="attrs" v-on="on">mdi-open-in-app</v-icon>
                </template>
                <span> Ver historia de usuario </span>
              </v-tooltip>
            </router-link>
          </template>
          <template #item.user="{ value }">
            <UserPill :user="value" />
          </template>
          <template #item.role="{ value }">
            {{ effortRolesMap[value].label }}
          </template>
          <template #item.effort="{ value }">
            <v-tooltip bottom>
              <template #activator="{ on, attrs }">
                <span v-bind="attrs" v-on="on">{{ value }}&nbsp;UT</span>
              </template>
              <span>{{ value * 0.5 }}&nbsp;h</span>
            </v-tooltip>
          </template>
          <template #item.comments="{ value }">
            <TruncatedText :value="value" :text-length="70" />
          </template>
        </ItemIndex>
      </v-col>
    </v-row>
    <EffortReportDialog ref="reportDialog" />
  </v-container>
</template>

<script>
import { toRefs } from "@vue/composition-api";
import { DateTime } from "luxon";

import Effort from "@/modules/scrum/models/effort";

import EffortFilters from "@/modules/scrum/components/filters/EffortFilters";
import EffortForm from "@/modules/scrum/components/forms/EffortForm";
import EffortReportDialog from "@/modules/scrum/components/dialogs/EffortReportDialog";

import { useMainStore } from "@/stores/main";
import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import { userHasPermission } from "@/utils/permissions";

export default {
  name: "EffortListView",
  metaInfo: {
    title: "Esfuerzo",
  },
  components: { EffortReportDialog },
  setup(props, { refs }) {
    // Store
    const mainStore = useMainStore();
    const userStoryStore = useUserStoryStore();

    // State
    const modelClass = Effort;
    const tableHeaders = [
      { text: "Fecha", align: "start", sortable: true, value: "date", fixed: true },
      {
        text: "Historia de usuario",
        align: "start",
        sortable: true,
        value: "user_story",
        sortingField: "user_story__name",
        fields: ["user_story.id", "user_story.name"],
        fixed: true,
      },
      {
        text: "Usuario",
        align: "start",
        sortable: true,
        value: "user",
        sortingField: "user__acronym",
        default: userHasPermission("scrum.view_effort"),
      },
      { text: "Rol", align: "start", sortable: false, value: "role", fixed: true },
      { text: "Esfuerzo", align: "start", sortable: true, value: "effort", fixed: true },
      { text: "Comentarios", align: "start", sortable: true, value: "comments", default: true },
      {
        text: "Acciones",
        align: "start",
        sortable: false,
        value: "table_actions",
        fields: ["user", "creation_datetime"],
        fixed: true,
      },
    ];
    const tableOptions = {
      sortBy: ["date", "user_story"],
      sortDesc: [true, false],
      mustSort: false,
      multiSort: true,
    };
    const filterComponent = EffortFilters;
    const systemFilters = userHasPermission(modelClass.VIEW_PERMISSION) ? {} : { user_id: mainStore.currentUser.id };
    const quickFilters = [
      {
        key: "last-week",
        label: "Última semana",
        filters: {
          date__gte: DateTime.local().minus({ weeks: 1 }).toISODate(),
          date__lte: DateTime.local().toISODate(),
        },
      },
    ];
    const formComponent = EffortForm;

    // Computed
    const { effortRolesMap } = toRefs(userStoryStore);

    // Methods
    function canPerformAction(item, action) {
      if (userHasPermission(`scrum.${action}_effort`)) {
        return true;
      }
      if (item.user !== mainStore.currentUser.id) {
        return false;
      }
      const limitDatetime = DateTime.local().minus({ minutes: 30 });
      return DateTime.fromISO(item.creation_datetime) > limitDatetime;
    }
    function openReportDialog(filters) {
      refs.reportDialog.open(filters);
    }

    return {
      // State
      modelClass,
      tableHeaders,
      tableOptions,
      filterComponent,
      systemFilters,
      quickFilters,
      formComponent,
      // Computed
      effortRolesMap,
      // Methods
      canPerformAction,
      openReportDialog,
    };
  },
};
</script>

<style scoped>
.user-story-link {
  text-decoration: none;
}
</style>
