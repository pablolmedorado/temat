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
          <v-btn icon :disabled="isLoading" @click="refresh">
            <v-icon>mdi-refresh</v-icon>
          </v-btn>
        </v-toolbar-items>
      </v-toolbar>
      <v-card-text class="mt-2">
        <v-row>
          <v-col>
            <v-chip v-if="filters && filters.date__gte" class="mr-2" color="teal" dark>
              <v-avatar tile left>
                <v-icon>mdi-calendar-start</v-icon>
              </v-avatar>
              {{ filters.date__gte }}
            </v-chip>
            <v-chip v-if="filters && filters.date__lte" class="mr-2" color="teal" dark>
              <v-avatar tile left>
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
        <v-row v-if="showUserChart">
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
import { computed, ref } from "@vue/composition-api";

import Effort from "@/modules/scrum/models/effort";

import EffortRoleTimelineChart from "@/modules/scrum/components/charts/EffortRoleTimelineChart";
import EffortUserTimelineChart from "@/modules/scrum/components/charts/EffortUserTimelineChart";

import { useUserStore } from "@/stores/users";

import useLoading from "@/composables/useLoading";
import useDialog, { dialogProps } from "@/composables/useDialog";
import { userHasPermission } from "@/utils/permissions";

export default {
  name: "EffortReportDialog",
  components: { EffortRoleTimelineChart, EffortUserTimelineChart },
  inheritAttrs: false,
  props: dialogProps,
  setup(props, { refs }) {
    // Store
    const userStore = useUserStore();

    // Composables
    const { isLoading } = useLoading({
      includedChildren: ["userChart", "roleChart"],
    });
    const { showDialog, open: _open, close } = useDialog(props);

    // State
    const filters = ref(null);
    const showUserChart = userHasPermission(Effort.VIEW_PERMISSION);

    // Computed
    const filteredUsers = computed(() => {
      if (!filters.value.user_id__in) {
        return undefined;
      }
      return filters.value.user_id__in
        .split(",")
        .map((user) => userStore.userMap[user].acronym)
        .join(", ");
    });

    // Methods
    async function open(newFilters) {
      filters.value = newFilters;
      await _open();
      refresh();
    }
    function refresh() {
      if (showUserChart) {
        refs.userChart.fetchData();
      }
      refs.roleChart.fetchData();
    }

    return {
      // State
      isLoading,
      showDialog,
      filters,
      showUserChart,
      // Computed
      filteredUsers,
      // Methods
      open,
      close,
      refresh,
    };
  },
};
</script>
