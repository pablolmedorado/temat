<script>
import { mapGetters } from "vuex";
import { get } from "lodash";
import colors from "vuetify/lib/util/colors";

import SprintService from "@/modules/scrum/services/sprint-service";

import BaseChart from "@/components/charts/BaseChart";

import { truncate } from "@/filters";

export default {
  name: "SprintGanttChart",
  extends: BaseChart,
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
  data() {
    return {
      constructorType: "ganttChart",
      service: SprintService,
      fetchFunctionName: "ganttChartData",
    };
  },
  computed: {
    ...mapGetters("scrum", ["riskLevelsMap"]),
    localChartOptions() {
      const router = this.$router;
      function navigateToUSDetail(event) {
        const userStoryId = event.point.id;
        router.push({ name: "user-story", params: { id: userStoryId } });
      }
      const userStories = get(this.chartData, "user_stories", []);

      return {
        title: {
          text: this.chartData.name,
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
          min: new Date(this.chartData.start_date).getTime(),
          max: new Date(this.chartData.end_date).getTime(),
        },
        series: [
          {
            name: this.chartData.name,
            data: userStories.map((userStory) => ({
              id: userStory.id,
              name: truncate(userStory.name, 35),
              start: new Date(userStory.start_date).getTime(),
              end: new Date(userStory.end_date).getTime(),
              completed: userStory.current_progress / 100,
              color: this.getUserStoryColour(userStory),
            })),
          },
        ],
      };
    },
  },
  methods: {
    buildFetchFunctionArgs() {
      return [this.sprintId];
    },
    getUserStoryColour(userStory) {
      if (userStory.risk_level !== 0) {
        return this.riskLevelsMap[userStory.risk_level].colour;
      }
      if (userStory.validated) {
        return colors.green.base;
      }
      if (!userStory.current_progress) {
        return colors.grey.base;
      }
      return colors.blue.base;
    },
  },
};
</script>
