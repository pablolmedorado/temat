<template>
  <v-container fluid>
    <ContextBreadcrumbs :items="breadcrumbs" />
    <v-card class="mt-2">
      <v-toolbar flat>
        <v-toolbar-title class="text-h6"> Informe de despliegue </v-toolbar-title>
        <v-spacer />
        <SprintViewSelector :sprint-id="sprintId" />
        <v-divider vertical inset class="mx-1" />
        <v-btn icon :disabled="isTaskLoading('fetch-report-data')" @click="fetchData">
          <v-icon>mdi-refresh</v-icon>
        </v-btn>
      </v-toolbar>
      <v-expansion-panels v-model="panels" :disabled="isTaskLoading('fetch-report-data')" flat multiple hover>
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
              <v-badge inline color="secondary" :content="userStoryCount.toString()">
                Historias de usuario ({{ progress }}%)
              </v-badge>
            </span>
          </v-expansion-panel-header>
          <v-expansion-panel-content>
            <v-data-table
              :headers="userStoryHeaders"
              :options="userStoryTableOptions"
              :items="visibleUserStories"
              :item-class="(item) => `risk-${item.risk_level}`"
              :loading="isTaskLoading('fetch-user-stories')"
              disable-pagination
              hide-default-footer
            >
              <template #top>
                <v-row class="d-flex align-center">
                  <v-col cols="12" sm="6" md>
                    <v-text-field v-model="userStoryNameFilter" label="Buscar" prepend-icon="mdi-magnify" clearable />
                  </v-col>
                  <v-col cols="12" sm="6" md>
                    <v-select
                      v-model="userStoryTypeFilter"
                      :items="userStoryTypesOptions"
                      item-text="name"
                      item-value="id"
                      label="Tipo"
                      prepend-icon="mdi-shape"
                      :loading="!userStoryTypesOptions.length"
                      clearable
                    />
                  </v-col>
                  <v-col cols="12" sm="6" md>
                    <TagAutocomplete
                      v-model="userStoryTagFilter"
                      label="Tags"
                      prepend-icon="mdi-label"
                      multiple
                      truncate-results
                      clearable
                    />
                  </v-col>
                  <v-col cols="auto">
                    <v-btn color="primary" rounded outlined @click="clearUserStoryFilters">
                      <v-icon>mdi-filter-off</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </template>

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
                <UserPill v-if="value" :user="value" />
              </template>
              <template #item.status="{ item }">
                <UserStoryIndexStatus :user-story="item" />
              </template>
              <template #item.classification="{ item }">
                <v-chip class="mr-1 my-1" color="info" outlined small label @click="userStoryTypeFilter = item.type">
                  <v-icon small left>mdi-shape</v-icon>
                  {{ userStoryTypesMap[item.type].name }}
                </v-chip>
                <TagLabels
                  v-if="item.tags"
                  :tags="item.tags"
                  small
                  @click:tag="userStoryTagFilter = uniq([...userStoryTagFilter, $event])"
                />
              </template>
              <template #item.misc="{ item }">
                <span class="d-inline-flex">
                  <v-menu
                    v-if="item.risk_comments"
                    :close-on-content-click="false"
                    :nudge-width="200"
                    open-on-hover
                    max-width="400px"
                    offset-x
                    left
                  >
                    <template #activator="{ on, attrs }">
                      <v-icon v-bind="attrs" class="mr-2 misc-icon" v-on="on">mdi-alert-decagram</v-icon>
                    </template>
                    <v-card>
                      <v-card-title class="text-subtitle-1">Comentarios de riesgo</v-card-title>
                      <v-card-text class="text-pre-wrap">{{ item.risk_comments }}</v-card-text>
                    </v-card>
                  </v-menu>
                  <v-tooltip left>
                    <template #activator="{ on, attrs }">
                      <v-icon v-if="item.use_migrations" v-bind="attrs" class="mr-2 misc-icon" v-on="on">
                        mdi-database-arrow-right
                      </v-icon>
                    </template>
                    <span> Tiene migraciones </span>
                  </v-tooltip>
                  <v-menu
                    v-if="item.deployment_notes"
                    :close-on-content-click="false"
                    :nudge-width="200"
                    open-on-hover
                    max-width="400px"
                    offset-x
                    left
                  >
                    <template #activator="{ on, attrs }">
                      <v-icon v-bind="attrs" class="misc-icon" v-on="on">mdi-note-text</v-icon>
                    </template>
                    <v-card>
                      <v-card-title class="text-subtitle-1">Notas de despliegue</v-card-title>
                      <v-card-text class="text-pre-wrap">{{ item.deployment_notes }}</v-card-text>
                    </v-card>
                  </v-menu>
                </span>
              </template>
            </v-data-table>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </v-container>
</template>

<script>
import { computed, nextTick, ref, watch } from "@vue/composition-api";
import { get, intersection, uniq } from "lodash-es";

import SprintService from "@/modules/scrum/services/sprint-service";
import UserStoryService from "@/modules/scrum/services/user-story-service";

import ContextBreadcrumbs from "@/modules/scrum/components/ContextBreadcrumbs";
import SprintViewSelector from "@/modules/scrum/components/SprintViewSelector";
import UserStoryIndexStatus from "@/modules/scrum/components/UserStoryIndexStatus";

import { useLoading } from "@/composables/loading";
import { useScrumContext } from "@/modules/scrum/composables/scrum-context";
import { useUserStoryTypes } from "@/modules/scrum/composables/user-story-types";

import { defaultTableOptions } from "@/utils/constants";

export default {
  name: "SprintDeploymentReportView",
  metaInfo() {
    return {
      title: `${get(this.contextItem, "name", "Sprint")} - Informe de despliegue`,
    };
  },
  components: { ContextBreadcrumbs, SprintViewSelector, UserStoryIndexStatus },
  props: {
    sprintId: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    // Composables
    const { isLoading, isTaskLoading, addTask, removeTask } = useLoading();
    const { contextItem } = useScrumContext();
    const { userStoryTypes: userStoryTypesOptions, userStoryTypesMap } = useUserStoryTypes();

    // State
    const panels = ref([]);
    const progress = ref(0);
    const userStoryCount = ref(0);
    const userStoriesWithMigrations = ref([]);
    const developmentUsers = ref([]);
    const deploymentNotes = ref([]);
    const userStoryHeaders = [
      {
        text: "Nombre",
        align: "start",
        sortable: true,
        value: "name",
      },
      { text: "Prioridad", sortable: true, value: "priority" },
      { text: "Responsable", sortable: false, value: "development_user" },
      { text: "Estado", sortable: true, value: "status" },
      {
        text: "Clasificación",
        sortable: false,
        value: "classification",
        fields: ["tags.name", "tags.colour", "tags.icon"],
      },
      { text: "Miscelánea", sortable: false, value: "misc" },
    ];
    const userStoryTableOptions = {
      ...defaultTableOptions,
      sortBy: ["status", "priority"],
      sortDesc: [false, false],
      multiSort: true,
      mustSort: true,
    };
    const userStories = ref([]);
    const userStoryNameFilter = ref("");
    const userStoryTypeFilter = ref(null);
    const userStoryTagFilter = ref([]);
    const visibleUserStories = ref([]);

    // Computed
    const breadcrumbs = computed(() => {
      if (contextItem.value) {
        return [
          {
            text: "Sprints",
            to: { name: "sprints" },
            exact: true,
          },
          { text: contextItem.value.name, disabled: false, link: false },
          { text: "Informe de despliegue", disabled: true },
        ];
      } else {
        return [];
      }
    });

    // Watchers
    watch(userStories, (newValue) => (visibleUserStories.value = newValue));
    watch([userStoryNameFilter, userStoryTypeFilter, userStoryTagFilter], filterUserStories);

    // Methods
    async function fetchData() {
      addTask("fetch-report-data");
      try {
        panels.value = [];
        userStories.value = [];
        const response = await SprintService.deploymentReportData(props.sprintId);
        developmentUsers.value = get(response, ["data", "development_users"], []);
        if (developmentUsers.value.length) {
          panels.value.push(0);
        }
        userStoriesWithMigrations.value = get(response, ["data", "user_stories_with_migrations"], []);
        if (userStoriesWithMigrations.value.length) {
          panels.value.push(1);
        }
        deploymentNotes.value = get(response, ["data", "deployment_notes"], []);
        if (deploymentNotes.value.length) {
          panels.value.push(2);
        }
        progress.value = get(response, ["data", "progress"], 0);
        userStoryCount.value = get(response, ["data", "user_story_count"], 0);
      } finally {
        removeTask("fetch-report-data");
      }
    }
    function fetchUserStories(forceFetch) {
      nextTick(async () => {
        if (panels.value.includes(3) && (!userStories.value.length || forceFetch)) {
          addTask("fetch-user-stories");
          try {
            const response = await UserStoryService.list({
              sprint_id: props.sprintId,
              fields:
                "id,name,type,priority,status,current_progress,validated,development_user,risk_level,risk_comments," +
                "use_migrations,deployment_notes,tags",
              expand: "tags",
              ordering: "status,priority",
            });
            userStories.value = response.data;
            userStoryCount.value = response.data.length;
          } finally {
            removeTask("fetch-user-stories");
          }
        }
      });
    }
    function filterUserStories() {
      visibleUserStories.value = userStories.value
        .filter((us) =>
          userStoryNameFilter.value ? us.name.toLowerCase().includes(userStoryNameFilter.value.toLowerCase()) : true
        )
        .filter((us) => (userStoryTypeFilter.value ? us.type === userStoryTypeFilter.value : true))
        .filter((us) => {
          return get(userStoryTagFilter.value, "length")
            ? intersection(
                us.tags.map((tag) => tag.name),
                userStoryTagFilter.value
              ).length === userStoryTagFilter.value.length
            : true;
        });
    }
    function clearUserStoryFilters() {
      userStoryNameFilter.value = "";
      userStoryTypeFilter.value = null;
      userStoryTagFilter.value = [];
      visibleUserStories.value = userStories.value;
    }

    // Initialization
    fetchData();
    fetchUserStories(true);

    return {
      // State
      panels,
      progress,
      userStoryCount,
      userStoriesWithMigrations,
      developmentUsers,
      deploymentNotes,
      userStoryHeaders,
      userStoryTableOptions,
      userStoryNameFilter,
      userStoryTypeFilter,
      userStoryTagFilter,
      visibleUserStories,
      // Computed
      isLoading,
      contextItem,
      userStoryTypesOptions,
      userStoryTypesMap,
      breadcrumbs,
      // Methods
      get,
      uniq,
      isTaskLoading,
      fetchData,
      fetchUserStories,
      filterUserStories,
      clearUserStoryFilters,
    };
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
.misc-icon {
  cursor: help !important;
}
.v-data-table ::v-deep .v-data-table-header th {
  white-space: nowrap;
}
::v-deep tr.risk-1 {
  background-color: rgba(255, 152, 0, 0.2);
}
::v-deep tr.risk-2 {
  background-color: rgba(244, 67, 54, 0.2);
}
</style>
