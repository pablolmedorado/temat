import { keyBy } from "lodash-es";

import NotificationService from "./notification-service";

const services = keyBy([NotificationService], "basename");

export default services;
