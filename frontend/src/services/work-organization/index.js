import { keyBy } from "lodash";

import GreenDayService from "./green-service";
import HolidayService from "./holiday-service";
import SupportService from "./support-service";

const services = keyBy([GreenDayService, HolidayService, SupportService], "baseUrlName");

export default services;
