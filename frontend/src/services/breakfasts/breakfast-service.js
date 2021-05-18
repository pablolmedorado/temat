import BaseService from "../base-service";

class BreakfastService extends BaseService {
  baseUrlName = "breakfasts:breakfast";
}

const service = Object.freeze(new BreakfastService());

export default service;
