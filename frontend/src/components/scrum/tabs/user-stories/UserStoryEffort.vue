<template>
  <v-row>
    <v-col>
      <ItemIndex
        v-if="userStory.id"
        ref="itemIndex"
        local-storage-key="userStoryEffort"
        verbose-name="Esfuerzo"
        verbose-name-plural="Esfuerzo"
        item-text="date"
        :table-available-headers="tableHeaders"
        :table-initial-options="tableOptions"
        :system-filters="systemFilters"
        :service="service"
        :form-component="formComponent"
        :default-item="defaultItem"
        :can-create="() => true"
        :can-edit="canModify"
        :can-delete="canModify"
        custom-headers
        @submit:form="onFormSubmit"
        @delete:item="onDeleteItem"
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
import { mapGetters, mapState } from "vuex";
import { DateTime } from "luxon";

import EffortService from "@/services/scrum/effort-service";

import EffortForm from "@/components/scrum/forms/EffortForm";

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
      service: EffortService,
      formComponent: EffortForm,
    };
  },
  computed: {
    ...mapState(["locale", "loggedUser"]),
    ...mapGetters("scrum", ["effortRolesMap"]),
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
        id: null,
        date: DateTime.local().toISODate(),
        user: this.loggedUser.id,
        role: this.loggedUserRole,
        user_story: this.userStory.id,
        effort: 1,
        comments: "",
      };
    },
  },
  mounted() {
    if (this.$refs.itemIndex) {
      this.$refs.itemIndex.fetchTableItems();
    }
  },
  methods: {
    canModify(item, user) {
      if (user.is_staff) {
        return true;
      }
      if (item.user !== user.id) {
        return false;
      }
      const limitDatetime = DateTime.local().minus({ minutes: 30 });
      return DateTime.fromISO(item.creation_datetime) > limitDatetime;
    },
    onFormSubmit() {
      this.$emit("change:effort");
    },
    onDeleteItem() {
      this.$emit("change:effort");
    },
  },
};
</script>
