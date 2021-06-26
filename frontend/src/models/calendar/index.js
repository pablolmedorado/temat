import { keyBy } from "lodash";

import Event from "./event";
import EventType from "./event-type";

const models = keyBy([Event, EventType], (model) => `${model.contentType.app}/${model.contentType.model}`);

export default models;
