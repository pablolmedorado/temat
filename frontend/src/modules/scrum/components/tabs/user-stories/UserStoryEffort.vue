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
              <span :class="`${userStory.planned_effort >= userStory.actual_effort ? 'green' : 'orange'}--text`">
                {{ userStory.actual_effort }} UT</span
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
import { mapState } from "pinia";
import { DateTime } from "luxon";

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
  data() {
    return {
      modelClass: Effort,
      tableHeaders: [
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
      ],
      tableOptions: {
        sortBy: ["date"],
        sortDesc: [true],
        multiSort: true,
      },
      formComponent: EffortForm,
    };
  },
  computed: {
    ...mapState(useMainStore, ["locale", "loggedUser"]),
    ...mapState(useUserStoryStore, ["effortRolesMap"]),
    systemFilters() {
      return {
        user_story_id: this.userStory.id,
      };
    },
    loggedUserRole() {
      switch (this.loggedUser.id) {
        case this.userStory.development_user:
          return "D";
        case this.userStory.validation_user:
          return "V";
        case this.userStory.support_user:
          return "S";
        default:
          return null;
      }
    },
    defaultItem() {
      return {
        ...this.modelClass.defaults,
        role: this.loggedUserRole,
        user_story: this.userStory.id,
      };
    },
  },
  watch: {
    "userStory.id": {
      handler() {
        this.$refs.itemIndex.fetchTableItems();
      },
    },
  },
  mounted() {
    if (this.$refs.itemIndex) {
      this.$refs.itemIndex.fetchTableItems();
    }
  },
  methods: {
    canPerformAction(item, action) {
      if (userHasPermission(`scrum.${action}_effort`)) {
        return true;
      }
      if (item.user !== this.loggedUser.id) {
        return false;
      }
      const limitDatetime = DateTime.local().minus({ minutes: 30 });
      return DateTime.fromISO(item.creation_datetime) > limitDatetime;
    },
  },
};
</script>
