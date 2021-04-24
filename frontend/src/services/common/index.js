import { keyBy } from "lodash";

import NotificationService from "./notification-service";
import TagService from "./tag-service";

const services = keyBy([NotificationService, TagService], "baseUrlName");

export default services;
