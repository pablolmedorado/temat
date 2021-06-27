import { keyBy } from "lodash";

import GroupService from "./group-service";
import UserService from "./user-service";

const services = keyBy([GroupService, UserService], "basename");

export default services;
