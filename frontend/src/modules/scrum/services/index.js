import { keyBy } from "lodash";

import EffortService from "./effort-service";
import EpicService from "./epic-service";
import SprintService from "./sprint-service";
import TaskService from "./task-service";
import UserStoryService from "./user-story-service";
import UserStoryTypeService from "./user-story-type-service";

const services = keyBy(
  [EffortService, EpicService, SprintService, TaskService, UserStoryService, UserStoryTypeService],
  "basename"
);

export default services;
