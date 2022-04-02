import { keyBy } from "lodash-es";

import SupportService from "./support-service";

const services = keyBy([SupportService], "basename");

export default services;
