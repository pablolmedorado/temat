import { keyBy } from "lodash";

import SupportService from "./support-service";

const services = keyBy([SupportService], "basename");

export default services;
