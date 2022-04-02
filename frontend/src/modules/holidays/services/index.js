import { keyBy } from "lodash-es";

import HolidayService from "./holiday-service";

const services = keyBy([HolidayService], "basename");

export default services;
