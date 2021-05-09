import { keyBy } from "lodash";

import EventService from "./event-service";
import EventTypeService from "./event-type-service";

const services = keyBy([EventService, EventTypeService], "baseUrlName");

export default services;
