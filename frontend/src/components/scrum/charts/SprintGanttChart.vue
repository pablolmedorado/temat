<script>
import { mapGetters } from "vuex";
import { get } from "lodash";
import colors from "vuetify/lib/util/colors";

import SprintService from "@/services/scrum/sprint-service";

import BaseChart from "@/components/common/BaseChart";

import { truncate } from "@/filters";

export default {
  name: "SprintGanttChart",
  extends: BaseChart,
  props: {
    sprintId: {
      type: String,
      required: true
    },
    height: {
      type: Number,
      default: null
    }
  },
  data() {
    return {
      constructorType: "ganttChart",
      service: SprintService,
      fetchFunctionName: "ganttChartData"
    };
  },
  computed: {
    ...mapGetters("scrum", ["riskLevelsMap"]),
    localChartOptions() {
      const userStories = get(this.chartData, "user_stories", []);
      return {
        title: {
          text: this.chartData.name
        },
        legend: { enabled: false },
        xAxis: {
          min: new Date(this.chartData.start_date).getTime(),
          max: new Date(this.chartData.end_date).getTime()
        },
        series: [
          {
            name: this.chartData.name,
            data: userStories.map(userStory => ({
              name: truncate(userStory.name),
              start: new Date(userStory.start_date).getTime(),
              end: new Date(userStory.end_date).getTime(),
              completed: userStory.current_progress / 100,
              color: this.getUserStoryColour(userStory)
            }))
          }
        ]
      };
    }
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
    }
  }
};
</script>
