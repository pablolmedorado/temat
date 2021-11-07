import { keyBy } from "lodash";

import NotificationService from "./notification-service";

const services = keyBy([NotificationService], "basename");

export default services;
