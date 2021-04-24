import BaseService from "../base-service";

class UserStoryTypeService extends BaseService {
  baseUrlName = "scrum:user-story-type";
  defaultListParams = { ordering: "name" };
}

const service = Object.freeze(new UserStoryTypeService());

export default service;
