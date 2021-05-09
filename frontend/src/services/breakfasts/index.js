import { keyBy } from "lodash";

import BaseService from "./base-service";
import BreadService from "./bread-service";
import BreakfastService from "./breakfast-service";
import DrinkService from "./drink-service";
import IngredientService from "./ingredient-service";

const services = keyBy([BaseService, BreadService, BreakfastService, DrinkService, IngredientService], "baseUrlName");

export default services;
