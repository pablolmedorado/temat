import { keyBy } from "lodash-es";

import EventService from "./event-service";
import EventTypeService from "./event-type-service";

const services = keyBy([EventService, EventTypeService], "basename");

export default services;
