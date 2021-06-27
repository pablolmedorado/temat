import { keyBy } from "lodash";

import Effort from "./effort";
import Epic from "./epic";
import Sprint from "./sprint";
import Task from "./task";
import UserStory from "./user-story";
import UserStoryType from "./user-story-type";

const models = keyBy(
  [Effort, Epic, Sprint, Task, UserStory, UserStoryType],
  (model) => `${model.contentType.app}/${model.contentType.model}`
);

export default models;
