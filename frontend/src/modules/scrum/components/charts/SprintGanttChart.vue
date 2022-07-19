<template>
  <AsyncChart
    ref="chart"
    constructor-type="ganttChart"
    :options-function="buildOptions"
    :height="height"
    v-bind="{ ...$attrs, ...fetchProps }"
  />
</template>

<script>
import { computed } from "@vue/composition-api";
import { get } from "lodash-es";
import colors from "vuetify/lib/util/colors";

import { useUserStoryStore } from "@/modules/scrum/stores/user-stories";

import SprintService from "@/modules/scrum/services/sprint-service";

import { truncate } from "@/utils/text";

export default {
  name: "SprintGanttChart",
  inheritAttrs: false,
  props: {
    sprintId: {
      type: String,
      required: true,
    },
    height: {
      type: Number,
      default: null,
    },
  },
  setup(props, { refs, root }) {
    // Store
    const userStoryStore = useUserStoryStore();

    // Computed
    const fetchProps = computed(() => ({
      service: SprintService,
      fetchFunctionName: "ganttChartData",
      fetchFunctionArgs: [props.sprintId],
    }));

    // Methods
    function getUserStoryColour(userStory) {
      if (userStory.risk_level !== 0) {
        return userStoryStore.riskLevelsMap[userStory.risk_level].colour;
      }
      if (userStory.validated) {
        return colors.green.base;
      }
      if (!userStory.current_progress) {
        return colors.grey.base;
      }
      return colors.blue.base;
    }
    function buildOptions(chartData) {
      const router = root.$router;
      function navigateToUSDetail(event) {
        const userStoryId = event.point.id;
        router.push({ name: "user-story", params: { id: userStoryId } });
      }
      const userStories = get(chartData, "user_stories", []);

      return {
        title: {
          text: chartData.name,
        },
        legend: { enabled: false },
        tooltip: { shared: false },
        plotOptions: {
          series: {
            cursor: "pointer",
            point: {
              events: {
                click: navigateToUSDetail,
              },
            },
          },
        },
        xAxis: {
          currentDateIndicator: true,
          min: new Date(chartData.start_date).getTime(),
          max: new Date(chartData.end_date).getTime(),
        },
        series: [
          {
            name: chartData.name,
            data: userStories.map((userStory) => ({
              id: userStory.id,
              name: truncate(userStory.name, 35),
              start: new Date(userStory.start_date).getTime(),
              end: new Date(userStory.end_date).getTime(),
              completed: userStory.current_progress / 100,
              color: getUserStoryColour(userStory),
            })),
          },
        ],
      };
    }
    function fetchData() {
      refs.chart.fetchData();
    }

    return {
      // Computed
      fetchProps,
      // Methods
      buildOptions,
      fetchData,
    };
  },
};
</script>
