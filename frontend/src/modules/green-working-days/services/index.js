import { keyBy } from "lodash-es";

import GreenDayService from "./green-working-day-service";

const services = keyBy([GreenDayService], "basename");

export default services;
