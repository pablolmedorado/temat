<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card>
          <v-toolbar flat>
            <v-toolbar-title class="text-h6">Análisis ({{ year }})</v-toolbar-title>
            <v-spacer />
            <v-menu bottom left offset-y>
              <template #activator="{ on: menu }">
                <v-tooltip bottom>
                  <template #activator="{ on: tooltip }">
                    <v-btn icon :disabled="isLoading" v-on="{ ...tooltip, ...menu }">
                      <v-icon>mdi-calendar-range</v-icon>
                    </v-btn>
                  </template>
                  <span>Año</span>
                </v-tooltip>
              </template>
              <v-list>
                <v-list-item v-for="item in yearOptions" :key="item" @click="year = item">
                  <v-list-item-title>{{ item }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </v-toolbar>
          <v-card-text>
            <v-tabs fixed-tabs show-arrows="mobile">
              <v-tabs-slider />
              <v-tab href="#events"><v-icon>mdi-calendar-month</v-icon></v-tab>
              <v-tab href="#scrum"><v-icon>mdi-cards</v-icon></v-tab>
              <v-tab href="#support"><v-icon>mdi-face-agent</v-icon></v-tab>
              <v-tab href="#green"><v-icon>mdi-briefcase</v-icon></v-tab>
              <v-tab href="#holidays"><v-icon>mdi-beach</v-icon></v-tab>

              <v-tab-item value="events" class="pt-4">
                <v-row>
                  <v-col cols="12" lg="6">
                    <v-card outlined>
                      <v-card-text>
                        <EventMonthlyChart ref="eventMonthlyChart" :filter="{ start_datetime__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6" lg="3">
                    <v-card outlined>
                      <v-card-text>
                        <EventTypeChart ref="eventTypeChart" :filter="{ start_datetime__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6" lg="3">
                    <v-card outlined>
                      <v-card-text>
                        <EventAttendeesChart ref="eventAttendeesChart" :filter="{ start_datetime__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-tab-item>
              <v-tab-item value="scrum" class="pt-4">
                <v-row>
                  <v-col cols="12" md="6" lg="3">
                    <v-card outlined>
                      <v-card-text>
                        <UserStoryTypeChart ref="userStoryTypeChart" :filter="{ sprint__end_date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6" lg="3">
                    <v-card outlined>
                      <v-card-text>
                        <EffortRoleChart ref="effortRoleChart" :filter="{ sprint__end_date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6" lg="3">
                    <v-card outlined>
                      <v-card-text>
                        <UserStoryDelayedChart ref="userStoryDelayedChart" :filter="{ sprint__end_date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                  <v-col cols="12" md="6" lg="3">
                    <v-card outlined>
                      <v-card-text>
                        <UserStoryOverworkedChart
                          ref="userStoryOverworkedChart"
                          :filter="{ sprint__end_date__year: year }"
                        />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-card outlined>
                      <v-card-text>
                        <UserStoryUserChart ref="userStoryUserChart" :filter="{ sprint__end_date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-tab-item>
              <v-tab-item value="support" class="pt-4">
                <v-row>
                  <v-col>
                    <v-card outlined>
                      <v-card-text>
                        <SupportUsersChart ref="supportUsersChart" :filter="{ date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-tab-item>
              <v-tab-item value="green" class="pt-4">
                <v-row>
                  <v-col>
                    <v-card outlined>
                      <v-card-text>
                        <GreenWorkingDaysChart ref="greenWorkingDaysChart" :filter="{ date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-tab-item>
              <v-tab-item value="holidays" class="pt-4">
                <v-row>
                  <v-col>
                    <v-card outlined>
                      <v-card-text>
                        <HolidaysChart ref="holidaysChart" :filter="{ allowance_date__year: year }" />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
                <v-row>
                  <v-col>
                    <v-card outlined>
                      <v-card-text>
                        <HolidaysDistributionChart
                          ref="holidaysDistributionChart"
                          :filter="{ allowance_date__year: year }"
                          :height="500"
                        />
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-tab-item>
            </v-tabs>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";
import { DateTime } from "luxon";

import EffortRoleChart from "@/components/scrum/charts/EffortRoleChart";
import EventAttendeesChart from "@/components/calendar/charts/EventAttendeesChart";
import EventMonthlyChart from "@/components/calendar/charts/EventMonthlyChart";
import EventTypeChart from "@/components/calendar/charts/EventTypeChart";
import GreenWorkingDaysChart from "@/components/work-organization/green-working-days/GreenWorkingDaysChart";
import HolidaysChart from "@/components/work-organization/holidays/charts/HolidaysChart";
import HolidaysDistributionChart from "@/components/work-organization/holidays/charts/HolidaysDistributionChart";
import SupportUsersChart from "@/components/work-organization/support/SupportUsersChart";
import UserStoryDelayedChart from "@/components/scrum/charts/UserStoryDelayedChart";
import UserStoryOverworkedChart from "@/components/scrum/charts/UserStoryOverworkedChart";
import UserStoryTypeChart from "@/components/scrum/charts/UserStoryTypeChart";
import UserStoryUserChart from "@/components/scrum/charts/UserStoryUserChart";

import useLoading from "@/composables/useLoading";

export default {
  name: "Analytics",
  metaInfo: {
    title: "Análisis",
  },
  components: {
    EffortRoleChart,
    EventAttendeesChart,
    EventMonthlyChart,
    EventTypeChart,
    GreenWorkingDaysChart,
    HolidaysChart,
    HolidaysDistributionChart,
    SupportUsersChart,
    UserStoryDelayedChart,
    UserStoryOverworkedChart,
    UserStoryTypeChart,
    UserStoryUserChart,
  },
  setup() {
    const { isLoading } = useLoading({
      includedChildren: [
        "eventMonthlyChart",
        "eventTypeChart",
        "eventAttendeesChart",
        "userStoryTypeChart",
        "effortRoleChart",
        "userStoryDelayedChart",
        "userStoryOverworkedChart",
        "userStoryUserChart",
        "supportUsersChart",
        "greenWorkingDaysChart",
        "holidaysChart",
        "holidaysDistributionChart",
      ],
    });
    return {
      isLoading,
    };
  },
  data() {
    return {
      year: DateTime.local().year,
    };
  },
  computed: {
    ...mapGetters(["yearOptions"]),
  },
};
</script>
