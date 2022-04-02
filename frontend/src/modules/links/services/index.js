import { keyBy } from "lodash-es";

import LinkService from "./link-service";

const services = keyBy([LinkService], "basename");

export default services;
