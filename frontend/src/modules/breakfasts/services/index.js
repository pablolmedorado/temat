import { keyBy } from "lodash-es";

import BaseService from "./base-service";
import BreadService from "./bread-service";
import BreakfastService from "./breakfast-service";
import DrinkService from "./drink-service";
import IngredientService from "./ingredient-service";

const services = keyBy([BaseService, BreadService, BreakfastService, DrinkService, IngredientService], "basename");

export default services;
