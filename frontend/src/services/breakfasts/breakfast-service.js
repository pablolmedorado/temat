import BaseService from "../base-service";

class BreakfastService extends BaseService {
  basename = "breakfasts:breakfast";
}

const service = Object.freeze(new BreakfastService());

export default service;
