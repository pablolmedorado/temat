<template>
  <v-card :style="borderStyle">
    <v-card-text class="py-0">
      <v-row>
        <v-col class="d-inline-flex">
          <v-tooltip v-if="userStory.status === 2" bottom>
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
          <router-link class="user-story-link text-h6" :to="{ name: 'user-story', params: { id: userStory.id } }">
            <TruncatedText :value="userStory.name" :text-length="70" />
          </router-link>
        </v-col>
      </v-row>
      <v-row>
        <v-col>
          <v-chip :color="effortPillColour" :text-color="effortPillColour" outlined>
            <v-avatar left :class="[effortPillColour, 'darken-4', 'white--text']">
              {{ userStory.current_effort }}
            </v-avatar>
            {{ userStory.planned_effort }} UT
            <v-avatar right>
              <v-icon>mdi-dumbbell</v-icon>
            </v-avatar>
          </v-chip>
        </v-col>
        <v-spacer />
        <v-col class="d-flex justify-end">
          <v-chip :color="endDatePillColour" :text-color="endDatePillColour" outlined>
            <v-avatar left :class="[endDatePillColour, 'darken-4', 'white--text']">
              {{ endDatePillNumber }}
            </v-avatar>
            {{ userStory.end_date }}
            <v-avatar right>
              <v-icon>mdi-bullseye-arrow</v-icon>
            </v-avatar>
          </v-chip>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script>
import { computed } from "@vue/composition-api";
import { get } from "lodash-es";
import { DateTime } from "luxon";
import colors from "vuetify/lib/util/colors";

import UserStoryActors from "@/modules/scrum/components/UserStoryActors";

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
  setup(props) {
    const borderStyle = computed(() => {
      const riskColours = [colors.green.base, colors.orange.base, colors.red.base];
      return {
        borderLeftColor: get(riskColours, [props.userStory.risk_level], colors.blue.base),
      };
    });
    const effortPillColour = computed(() => {
      return props.userStory.current_effort <= props.userStory.planned_effort ? "green" : "orange";
    });
    const endDatePillNumber = computed(() => {
      const startDate = DateTime.fromISO(props.userStory.start_date);
      const end = props.userStory.status < 4 ? DateTime.local() : DateTime.fromISO(props.userStory.validated_changed);
      return Math.max(0, Math.floor(end.diff(startDate).as("days")));
    });
    const endDatePillColour = computed(() => {
      const endDate = DateTime.fromISO(props.userStory.end_date).plus({ days: 1 });
      if (props.userStory.status < 4) {
        const now = DateTime.local();
        return endDate < now ? "orange" : "green";
      } else {
        const validationDate = DateTime.fromISO(props.userStory.validated_changed);
        return endDate <= validationDate ? "orange" : "green";
      }
    });

    return {
      borderStyle,
      effortPillColour,
      endDatePillNumber,
      endDatePillColour,
    };
  },
};
</script>

<style lang="scss" scoped>
.v-card {
  min-width: 325px;
  border-left-style: solid;
  border-left-width: 8px;
}
.user-story-link {
  color: unset;
  text-decoration: none;

  :hover {
    cursor: pointer !important;
  }
}
.progress {
  font-size: 14px;
}
::v-deep .v-progress-circular__info {
  font-size: 0.79rem;
}
</style>
