import { keyBy } from "lodash";

import HolidayService from "./holiday-service";

const services = keyBy([HolidayService], "basename");

export default services;
