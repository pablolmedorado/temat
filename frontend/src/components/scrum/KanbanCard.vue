<template>
  <v-card class="elevation-5" :style="borderStyle">
    <v-container fluid class="py-0">
      <v-row>
        <v-col class="d-inline-flex">
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-progress-circular
                class="mr-2"
                :rotate="-90"
                :size="32"
                :value="userStory.current_progress"
                :width="3"
                :color="userStory.validated ? 'green' : 'primary'"
                v-bind="attrs"
                v-on="on"
              >
                <span class="progress">
                  {{ userStory.current_progress }}
                </span>
              </v-progress-circular>
            </template>
            <span> Última actualización: {{ userStory.current_progress_changed | datetime }} </span>
          </v-tooltip>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-icon
                v-if="userStory.validated === false"
                class="mr-2"
                color="error"
                :size="32"
                v-bind="attrs"
                v-on="on"
              >
                mdi-alert-circle-check-outline
              </v-icon>
            </template>
            <span> Fecha de rechazo: {{ userStory.validated_changed | datetime }} </span>
          </v-tooltip>
          <v-chip color="secondary" text-color="secondary" outlined>
            <v-avatar left class="secondary darken-4 white--text">
              {{ userStory.priority }}
            </v-avatar>
            <v-avatar tile>
              <v-icon>mdi-priority-high</v-icon>
            </v-avatar>
          </v-chip>
        </v-col>
        <v-spacer />
        <v-col class="d-inline-flex justify-end">
          <UserStoryActors :user-story="userStory" :avatar-size="32" />
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <router-link class="title text-h6" :to="{ name: 'user-story', params: { id: userStory.id } }">
            <TruncatedText :value="userStory.name" :text-length="70" />
          </router-link>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-tooltip bottom>
            <template #activator="{ on, attrs }">
              <v-chip :color="effortPillColour" :text-color="effortPillColour" outlined v-bind="attrs" v-on="on">
                <v-avatar left :class="[effortPillColour, 'darken-4', 'white--text']">
                  {{ userStory.planned_effort }}
                </v-avatar>
                UT
                <v-avatar right>
                  <v-icon>mdi-dumbbell</v-icon>
                </v-avatar>
              </v-chip>
            </template>
            <span>Esfuerzo real: {{ userStory.actual_effort }}UT</span>
          </v-tooltip>
        </v-col>
        <v-spacer />
        <v-col class="d-flex justify-end">
          <v-chip :color="endDatePillColour" :text-color="endDatePillColour" outlined>
            <v-avatar left>
              <v-icon>mdi-bullseye-arrow</v-icon>
            </v-avatar>
            {{ userStory.end_date }}
          </v-chip>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import { DateTime } from "luxon";
import colors from "vuetify/lib/util/colors";

import UserStoryActors from "@/components/scrum/UserStoryActors";

import { isoDateTimeToLocaleString } from "@/utils/dates";

export default {
  name: "KanbanCard",
  components: { UserStoryActors },
  filters: {
    datetime: isoDateTimeToLocaleString,
  },
  props: {
    userStory: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      greenColour: colors.green.base,
      orangeColour: colors.orange.base,
      redColour: colors.red.base,
      blueColour: colors.blue.base,
    };
  },
  computed: {
    borderStyle() {
      const style = { borderLeftColor: undefined };
      switch (this.userStory.risk_level) {
        case 0:
          style.borderLeftColor = colors.green.base;
          break;
        case 1:
          style.borderLeftColor = colors.orange.base;
          break;
        case 2:
          style.borderLeftColor = colors.red.base;
          break;
        default:
          style.borderLeftColor = colors.blue.base;
      }
      return style;
    },
    effortPillColour() {
      return this.userStory.actual_effort <= this.userStory.planned_effort ? "green" : "orange";
    },
    endDatePillColour() {
      const endDate = DateTime.fromISO(this.userStory.end_date).plus({ days: 1 });
      if (this.userStory.status < 4) {
        const now = DateTime.local();
        return endDate < now ? "orange" : "green";
      } else {
        const validationDate = DateTime.fromISO(this.userStory.validated_changed);
        return endDate <= validationDate ? "orange" : "green";
      }
    },
  },
};
</script>

<style scoped>
.v-card {
  min-width: 285px;
  border-left-style: solid;
  border-left-width: 8px;
}
.title {
  color: unset;
  text-decoration: none;
}
.progress {
  font-size: 14px;
}
</style>
