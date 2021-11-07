import { keyBy } from "lodash";

import LinkService from "./link-service";

const services = keyBy([LinkService], "basename");

export default services;
