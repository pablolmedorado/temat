<template>
  <v-row>
    <v-col>
      <ItemIndex
        v-if="userStory.id"
        ref="itemIndex"
        :model-class="modelClass"
        local-storage-namespace="userStoryEffort"
        :table-available-headers="tableHeaders"
        :table-initial-options="tableOptions"
        :system-filters="systemFilters"
        :form-component="formComponent"
        :default-item="defaultItem"
        allow-add
        :allow-change="(user, item) => canPerformAction(item, 'change')"
        :allow-delete="(user, item) => canPerformAction(item, 'delete')"
        custom-headers
        @submit:form="$emit('change:effort')"
        @delete:item="$emit('change:effort')"
      >
        <template #top>
          <div class="px-4 pb-4 text-center">
            <span><strong>Esfuerzo planificado:</strong>&nbsp;{{ userStory.planned_effort }} UT</span> /
            <span>
              <strong>Esfuerzo real acumulado:</strong>&nbsp;
              <span :class="`${userStory.planned_effort >= userStory.current_effort ? 'green' : 'orange'}--text`">
                {{ userStory.current_effort }} UT</span
              >.
            </span>
          </div>
        </template>

        <template #item.date="{ value }">
          <DateRouterLink :date="value" />
        </template>
        <template #item.user="{ value }">
          <UserPill :user="value" />
        </template>
        <template #item.role="{ value }"> {{ effortRolesMap[value].label }}</template>
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
      <v-alert v-else type="info" text outlined border="left">
        Aún no ha creado la historia de usuario. Para poder añadir datos de esfuerzo, guarde los cambios primero.
      </v-alert>
    </v-col>
  </v-row>
</template>

<script>
import { computed, onMounted, toRefs, watch } from "@vue/composition-api";
import { DateTime } from "luxon";
import { invoke } from "lodash-es";

import Effort from "@/modules/scrum/models/effort";

import EffortForm from "@/modules/scrum/components/forms/EffortForm";

import { useMainStore } from "@/stores/main";
import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import { userHasPermission } from "@/utils/permissions";

export default {
  name: "UserStoryEffort",
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  setup(props, { refs }) {
    // Store
    const mainStore = useMainStore();
    const userStoryStore = useUserStoryStore();

    // State
    const modelClass = Effort;
    const tableHeaders = [
      { text: "Fecha", align: "start", sortable: true, value: "date", fixed: true },
      {
        text: "Usuario",
        align: "start",
        sortable: true,
        value: "user",
        sortingField: "user__acronym",
        fixed: true,
      },
      { text: "Rol", align: "start", sortable: false, value: "role", fixed: true },
      { text: "Esfuerzo", align: "start", sortable: true, value: "effort", fixed: true },
      { text: "Comentarios", align: "start", sortable: true, value: "comments", default: true },
      {
        text: "Acciones",
        align: "start",
        sortable: false,
        value: "table_actions",
        fields: ["user_story", "creation_datetime"],
        fixed: true,
      },
    ];
    const tableOptions = {
      sortBy: ["date"],
      sortDesc: [true],
      multiSort: true,
    };
    const formComponent = EffortForm;

    // Computed
    const { effortRolesMap } = toRefs(userStoryStore);
    const systemFilters = computed(() => ({ user_story_id: props.userStory.id }));
    const loggedUserRole = computed(() => {
      switch (mainStore.currentUser.id) {
        case props.userStory.development_user:
          return "D";
        case props.userStory.validation_user:
          return "V";
        case props.userStory.support_user:
          return "S";
        default:
          return null;
      }
    });
    const defaultItem = computed(() => ({
      ...modelClass.getDefaults(),
      role: loggedUserRole.value,
      user_story: props.userStory.id,
    }));

    // Watchers
    watch(
      () => props.userStory.id,
      () => invoke(refs, "itemIndex.fetchTableItems")
    );

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

    // Lifecycle hooks
    onMounted(() => invoke(refs, "itemIndex.fetchTableItems"));

    return {
      // State
      modelClass,
      tableHeaders,
      tableOptions,
      formComponent,
      // Computed
      effortRolesMap,
      systemFilters,
      defaultItem,
      // Methods
      canPerformAction,
    };
  },
};
</script>
