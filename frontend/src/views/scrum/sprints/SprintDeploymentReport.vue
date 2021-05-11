<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Informe de despliegue </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
        <v-divider vertical inset />
        <v-btn icon :disabled="loading" @click="fetchData">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      <v-expansion-panels v-model="panels" :disabled="loading" flat multiple hover>
        <v-expansion-panel>
          <v-expansion-panel-header class="panel-header">
            <span>
              <v-icon class="mr-2">mdi-account-alert</v-icon>
              <v-badge inline color="secondary" :content="developmentUsers.length.toString()">
                Desarrolladores implicados
              </v-badge>
            </span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-chip-group column>
              <UserPill v-for="(user, index) in developmentUsers" :key="`developer-${index}`" :user="user" />
            </v-chip-group>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header class="panel-header">
            <span>
              <v-icon class="mr-2">mdi-database-arrow-right</v-icon>
              <v-badge inline color="secondary" :content="userStoriesWithMigrations.length.toString()">
                Migraciones
              </v-badge>
            </span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            {{ userStoriesWithMigrations.length }} historias de usuario utilizan migraciones.
            <ul>
              <li v-for="userStory in userStoriesWithMigrations" :key="userStory.id">
                <router-link :to="{ name: 'user-story', params: { id: userStory.id } }">
                  {{ userStory.name }}
                </router-link>
              </li>
            </ul>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel>
          <v-expansion-panel-header class="panel-header">
            <span>
              <v-icon class="mr-2">mdi-note-text</v-icon>
              <v-badge inline color="secondary" :content="deploymentNotes.length.toString()">
                Notas de despliegue
              </v-badge>
            </span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <ul>
              <li v-for="userStory in deploymentNotes" :key="userStory.id">
                <span class="text-subtitle-1 font-weight-medium">
                  <router-link :to="{ name: 'user-story', params: { id: userStory.id } }">
                    {{ userStory.name }}
                  </router-link>
                </span>
                <p class="text-pre-wrap">{{ userStory.deployment_notes }}</p>
              </li>
            </ul>
          </v-expansion-panel-content>
        </v-expansion-panel>

        <v-expansion-panel @change="fetchUserStories">
          <v-expansion-panel-header class="panel-header">
            <span>
              <v-icon class="mr-2">mdi-book-account</v-icon>
              <v-badge inline color="secondary" :content="userStoryCount.toString()"> Historias de usuario </v-badge>
            </span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-data-table
              :headers="userStoryHeaders"
              :options="userStoryTableOptions"
              :items="userStories"
              :loading="loading"
              disable-pagination
              hide-default-footer
            >
              <template #item.name="{ item }">
                {{ item.name }}
                <router-link class="ml-1 user-story-link" :to="{ name: 'user-story', params: { id: item.id } }">
                  <v-tooltip bottom>
                    <template #activator="{ on, attrs }">
                      <v-icon small v-bind="attrs" v-on="on">mdi-open-in-app</v-icon>
                    </template>
                    <span> Ver historia de usuario </span>
                  </v-tooltip>
                </router-link>
              </template>
              <template #item.priority="{ value }">
                <v-icon>{{ `mdi-numeric-${value}-box` }}</v-icon>
              </template>
              <template #item.development_user="{ value }">
                <UserPill :user="value" />
              </template>
              <template #item.status="{ item }">
                <UserStoryIndexStatus :user-story="item" />
              </template>
              <template #item.use_migrations="{ item }">
                <v-simple-checkbox v-model="item.use_migrations" disabled />
              </template>
              <template #item.deployment_notes="{ value }">
                <TruncatedText :value="value" :text-length="100" />
              </template>
            </v-data-table>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { get } from "lodash";

import SprintService from "@/services/scrum/sprint-service";
import UserStoryService from "@/services/scrum/user-story-service";

import ContextBreadcrumbs from "@/components/scrum/ContextBreadcrumbs";
import SprintViewSelector from "@/components/scrum/SprintViewSelector";
import UserStoryIndexStatus from "@/components/scrum/UserStoryIndexStatus";

import useScrumContext from "@/composables/useScrumContext";
import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "SprintDeploymentReport",
  metaInfo: {
    title: "Sprint - Informe de despliegue",
  },
  components: { ContextBreadcrumbs, SprintViewSelector, UserStoryIndexStatus },
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const { contextItem } = useScrumContext(props);
    return {
      contextItem,
    };
  },
  data() {
    return {
      panels: [],
      userStoryCount: 0,
      userStoriesWithMigrations: [],
      developmentUsers: [],
      deploymentNotes: [],
      userStoryHeaders: [
        {
          text: "Nombre",
          align: "start",
          sortable: true,
          value: "name",
        },
        { text: "Prioridad", sortable: true, value: "priority" },
        { text: "Responsable", sortable: false, value: "development_user" },
        { text: "Estado", sortable: true, value: "status" },
        { text: "Migraciones", sortable: true, value: "use_migrations" },
        { text: "Notas", sortable: false, value: "deployment_notes" },
      ],
      userStoryTableOptions: {
        ...defaultTableOptions,
        sortBy: ["status", "priority"],
        sortDesc: [false, false],
        multiSort: true,
        mustSort: true,
      },
      userStories: [],
    };
  },
  computed: {
    ...mapGetters(["loading"]),
    breadcrumbs() {
      if (this.contextItem) {
        return [
          {
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          },
          { text: this.contextItem.name, disabled: false, link: false },
          { text: "Informe de despliegue", disabled: true },
        ];
      } else {
        return [];
      }
    },
  },
  created() {
    this.fetchData();
    this.fetchUserStories(true);
  },
  methods: {
    get,
    async fetchData() {
      this.panels = [];
      this.userStories = [];
      const response = await SprintService.deploymentReportData(this.sprintId);
      this.developmentUsers = get(response, ["data", "development_users"], []);
      if (this.developmentUsers.length) {
        this.panels.push(0);
      }
      this.userStoriesWithMigrations = get(response, ["data", "user_stories_with_migrations"], []);
      if (this.userStoriesWithMigrations.length) {
        this.panels.push(1);
      }
      this.deploymentNotes = get(response, ["data", "deployment_notes"], []);
      if (this.deploymentNotes.length) {
        this.panels.push(2);
      }
      this.userStoryCount = get(response, ["data", "user_story_count"], 0);
    },
    fetchUserStories(forceFetch) {
      this.$nextTick(async () => {
        if (this.panels.includes(3) && (!this.userStories.length || forceFetch)) {
          const response = await UserStoryService.list({
            sprint_id: this.sprintId,
            fields:
              "id,name,priority,status,current_progress,validated,development_user,risk_level,use_migrations,deployment_notes",
            ordering: "status,priority",
          });
          this.userStories = response.data;
          this.userStoryCount = response.data.length;
        }
      });
    },
  },
};
</script>

<style scoped>
.panel-header {
  font-weight: 700 !important;
  font-size: 1rem;
}
.user-story-link {
  text-decoration: none;
}
.text-pre-wrap {
  white-space: pre-wrap;
}
.v-data-table ::v-deep .v-data-table-header th {
  white-space: nowrap;
}
</style>
