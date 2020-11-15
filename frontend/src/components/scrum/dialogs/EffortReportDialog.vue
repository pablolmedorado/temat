<template>
  <v-dialog v-model="showDialog" v-bind="$attrs" fullscreen hide-overlay transition="dialog-bottom-transition">
    <v-card>
      <v-toolbar dark color="secondary">
        <v-btn icon dark @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
        <v-toolbar-title>Informe de esfuerzo</v-toolbar-title>
        <v-spacer />
        <v-toolbar-items>
          <v-btn icon :disabled="loading" @click="refresh">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card-text class="mt-2">
        <v-row>
          <v-col>
            <v-chip v-if="filters && filters.date__gte" class="mr-2" color="teal" dark>
              <v-avatar left>
                <v-icon>mdi-calendar-start</v-icon>
              </v-avatar>
              {{ filters.date__gte }}
            </v-chip>
            <v-chip v-if="filters && filters.date__lte" class="mr-2" color="teal" dark>
              <v-avatar left>
                <v-icon>mdi-calendar-end</v-icon>
              </v-avatar>
              {{ filters.date__lte }}
            </v-chip>
            <v-chip v-if="filters && filteredUsers" class="mr-2" color="teal" dark>
              <v-avatar left>
                <v-icon>mdi-account</v-icon>
              </v-avatar>
              {{ filteredUsers }}
            </v-chip>
          </v-col>
        </v-row>
        <v-row v-if="loggedUser.is_staff">
          <v-col>
            <v-card outlined>
              <EffortUserTimelineChart
                v-if="filters"
                ref="userChart"
                :filter="filters"
                :reactive-filters="false"
                :height="500"
              />
            </v-card>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-card outlined>
              <EffortRoleTimelineChart
                v-if="filters"
                ref="roleChart"
                :filter="filters"
                :reactive-filters="false"
                :height="500"
              />
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { mapGetters, mapState } from "vuex";

import DialogMixin from "@/mixins/dialog-mixin";

import EffortRoleTimelineChart from "@/components/scrum/charts/EffortRoleTimelineChart";
import EffortUserTimelineChart from "@/components/scrum/charts/EffortUserTimelineChart";

export default {
  name: "EffortReportDialog",
  components: { EffortRoleTimelineChart, EffortUserTimelineChart },
  mixins: [DialogMixin],
  data() {
    return {
      filters: null,
    };
  },
  computed: {
    ...mapState(["loggedUser"]),
    ...mapGetters(["loading"]),
    ...mapGetters("users", ["usersMap"]),
    filteredUsers() {
      if (!this.filters.user_id__in) {
        return undefined;
      }
      return this.filters.user_id__in
        .split(",")
        .map((user) => this.usersMap[user].acronym)
        .join(", ");
    },
  },
  methods: {
    open(filters) {
      this.filters = filters;
      this.showDialog = true;
      this.$nextTick(() => {
        this.refresh();
      });
    },
    close() {
      this.showDialog = false;
    },
    refresh() {
      if (this.loggedUser.is_staff) {
        this.$refs.userChart.getChartData();
      }
      this.$refs.roleChart.getChartData();
    },
  },
};
</script>
