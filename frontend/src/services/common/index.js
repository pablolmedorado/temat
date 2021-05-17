import { keyBy } from "lodash";

import LinkService from "./link-service";
import NotificationService from "./notification-service";
import TagService from "./tag-service";

const services = keyBy([LinkService, NotificationService, TagService], "baseUrlName");

export default services;
