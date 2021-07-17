import BaseService from "@/services/base-service";

class EpicService extends BaseService {
  basename = "scrum:epic";
}

const service = Object.freeze(new EpicService());

export default service;
