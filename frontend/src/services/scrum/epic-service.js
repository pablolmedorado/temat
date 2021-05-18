import BaseService from "../base-service";

class EpicService extends BaseService {
  baseUrlName = "scrum:epic";
}

const service = Object.freeze(new EpicService());

export default service;
