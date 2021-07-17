import BaseService from "@/services/base-service";

class BreadService extends BaseService {
  basename = "breakfasts:bread";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new BreadService());

export default service;
